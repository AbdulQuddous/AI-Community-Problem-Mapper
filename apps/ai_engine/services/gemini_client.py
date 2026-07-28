"""
Orchestrator for asynchronous complaint enrichment (FR18/FR19).

This function implements, in order, exactly the steps specified in
the Phase 2 sequence diagram (section 5.1). Each step's failure mode
is handled locally so that one failed Gemini call never prevents the
remaining steps from running or corrupts the complaint's saved state.
"""
import logging

from django.conf import settings

from apps.ai_engine.services import (
    classification_service,
    clustering_service,
    duplicate_service,
    embedding_service,
    language_service,
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

    # Step 1: language detection (local, always succeeds or defaults to unknown)
    complaint.language = language_service.detect_language(complaint.description)

    # Step 2: embedding generation (local, Sentence Transformers)
    try:
        complaint.embedding = embedding_service.generate_embedding(complaint.description)
    except Exception as exc:  # noqa: BLE001 — local model failure is unexpected but must not crash the thread
        logger.error("Embedding generation failed for complaint %s: %s", complaint.id, exc)
        complaint.save(update_fields=["language", "updated_at"])
        return  # without an embedding, duplicate check/clustering can't run meaningfully

    complaint.save(update_fields=["language", "embedding", "updated_at"])

    # Step 3: duplicate detection (local, FR8) — short-circuits remaining steps if matched
    duplicate = duplicate_service.find_duplicate(complaint)
    if duplicate:
        complaint.duplicate_of = duplicate
        complaint.save(update_fields=["duplicate_of", "updated_at"])
        logger.info("Complaint %s marked as duplicate of %s; enrichment stopped.", complaint.id, duplicate.id)
        return

    # Step 4: classification (Gemini, FR7) — degrade gracefully per FR19
    complaint.category = classification_service.classify_complaint(complaint.description)
    complaint.save(update_fields=["category", "updated_at"])

    if not complaint.category:
        logger.info("Complaint %s has no category (Gemini unavailable); skipping clustering/priority.", complaint.id)
        return

    # Step 5: clustering (local, DBSCAN, FR9/FR9A/FR11)
    cluster = clustering_service.assign_cluster(complaint)

    # Step 6: priority estimation (Gemini, FR10) — degrade gracefully per FR19
    complaint.priority_score = priority_service.estimate_priority(complaint, cluster)
    complaint.save(update_fields=["priority_score", "updated_at"])

    # Step 7: cluster summary (Gemini, FR12) — only when cluster is new/changed enough
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
    """
    Regenerate the summary when the cluster has no summary yet, or its
    size has grown by SUMMARY_REGEN_STEP since it's plausible the
    previous summary is now stale. See Phase 6 Architecture
    Discussion (2.6).
    """
    if not cluster.summary_text:
        return True
    return cluster.complaint_count % settings.SUMMARY_REGEN_STEP == 0