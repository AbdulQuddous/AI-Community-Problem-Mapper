"""
Orchestrator for asynchronous complaint enrichment (FR18/FR19).

Note: language detection step removed. The system is now scoped to
English-only submissions (enforced in ComplaintWriteSerializer at
submission time), so every complaint reaching this pipeline is
already guaranteed to be English — no per-complaint detection needed.

Note on step order: classification runs BEFORE duplicate detection so
duplicate_service can use category as a corroborating signal.
"""
import logging

from django.conf import settings

from apps.ai_engine.services import (
    classification_service,
    clustering_service,
    duplicate_service,
    embedding_service,
    local_classifier_service,
    priority_service,
    summarization_service,
)

logger = logging.getLogger("ai_engine")


def enrich_complaint(complaint_id: str) -> None:
    """
    Run full AI enrichment for a single complaint, out-of-band from
    the request/response cycle. Never raises — all failure modes are
    caught and logged internally, since this runs on a daemon thread
    with no caller to propagate exceptions to.
    """
    from apps.complaints.models import Complaint

    try:
        complaint = Complaint.objects.get(id=complaint_id)
    except Complaint.DoesNotExist:
        logger.error("Enrichment skipped: Complaint %s not found.", complaint_id)
        return

    # Step 1: embedding generation (local, Sentence Transformers)
    try:
        complaint.embedding = embedding_service.generate_embedding(complaint.description)
    except Exception as exc:  # noqa: BLE001
        logger.error("Embedding generation failed for complaint %s: %s", complaint.id, exc)
        complaint.save(update_fields=["updated_at"])
        return

    complaint.save(update_fields=["embedding", "updated_at"])

    # Step 2: classification — local model first, Gemini as fallback (FR7)
    complaint.category = local_classifier_service.classify_complaint_local(complaint.embedding)
    if not complaint.category:
        logger.info("Local classifier unavailable/uncertain for complaint %s; falling back to Gemini.", complaint.id)
        complaint.category = classification_service.classify_complaint(complaint.description)
    complaint.save(update_fields=["category", "updated_at"])

    # Step 3: duplicate detection (local, FR8) — category-aware
    duplicate = duplicate_service.find_duplicate(complaint)
    if duplicate:
        complaint.duplicate_of = duplicate
        complaint.save(update_fields=["duplicate_of", "updated_at"])
        logger.info("Complaint %s marked as duplicate of %s; enrichment stopped.", complaint.id, duplicate.id)
        return

    if not complaint.category:
        logger.info("Complaint %s has no category (local + Gemini both unavailable); skipping clustering/priority.", complaint.id)
        return

    # Step 4: clustering (local, DBSCAN, FR9/FR9A/FR11)
    cluster = clustering_service.assign_cluster(complaint)

    # Step 5: priority estimation (Gemini, FR10)
    complaint.priority_score = priority_service.estimate_priority(complaint, cluster)
    complaint.save(update_fields=["priority_score", "updated_at"])

    # Step 6: cluster summary (Gemini, FR12)
    if cluster and _should_regenerate_summary(cluster):
        summary = summarization_service.summarize_cluster(cluster)
        if summary:
            cluster.summary_text = summary
            cluster.save(update_fields=["summary_text", "updated_at"])

    logger.info(
        "Enrichment complete for complaint %s: category=%s priority=%s cluster=%s",
        complaint.id, complaint.category, complaint.priority_score,
        cluster.id if cluster else None,
    )


def _should_regenerate_summary(cluster) -> bool:
    if not cluster.summary_text:
        return True
    return cluster.complaint_count % settings.SUMMARY_REGEN_STEP == 0