"""
Orchestrator for asynchronous complaint enrichment (FR18/FR19).

Note: language detection step removed (English-only system).
Note on step order: classification runs BEFORE duplicate detection.

Note on duplicate handling: when a complaint is found to be a
duplicate, clustering/priority/summary are re-run on the ORIGINAL
complaint, not skipped entirely. A duplicate is real evidence that a
hotspot exists or has grown — without this, complaints that get
merged as duplicates would never contribute to cluster formation,
and a genuinely urgent, frequently-reported issue could end up with
no cluster and no AI summary at all, simply because every report
after the first was short-circuited before reaching clustering.
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

        # The duplicate itself doesn't get clustered/prioritized, but
        # it IS real evidence that the original's hotspot just grew.
        # Re-run clustering/priority/summary on the ORIGINAL so a
        # growing group of duplicates still produces a cluster and
        # an AI summary, instead of silently having neither.
        _cluster_prioritize_summarize(duplicate)
        return

    if not complaint.category:
        logger.info("Complaint %s has no category (local + Gemini both unavailable); skipping clustering/priority.", complaint.id)
        return

    # Steps 4-6: clustering, priority, summary — shared helper, also
    # used above when a duplicate arrives for an existing complaint.
    _cluster_prioritize_summarize(complaint)

    logger.info(
        "Enrichment complete for complaint %s: category=%s priority=%s cluster=%s",
        complaint.id, complaint.category, complaint.priority_score,
        complaint.cluster_id,
    )


def _cluster_prioritize_summarize(complaint) -> None:
    """
    Runs clustering, priority estimation, and (conditional) summary
    generation for a single complaint. Extracted as a shared helper
    so both the normal enrichment path and the "a duplicate just
    arrived, refresh the original's cluster" path use identical
    logic — avoids duplicating this three-step sequence.
    """
    cluster = clustering_service.assign_cluster(complaint)

    complaint.priority_score = priority_service.estimate_priority(complaint, cluster)
    complaint.save(update_fields=["priority_score", "updated_at"])

    if cluster and _should_regenerate_summary(cluster):
        summary = summarization_service.summarize_cluster(cluster)
        if summary:
            cluster.summary_text = summary
            cluster.save(update_fields=["summary_text", "updated_at"])

    logger.info(
        "Cluster/priority refreshed for complaint %s: priority=%s cluster=%s",
        complaint.id, complaint.priority_score, cluster.id if cluster else None,
    )


def _should_regenerate_summary(cluster) -> bool:
    if not cluster.summary_text:
        return True
    return cluster.complaint_count % settings.SUMMARY_REGEN_STEP == 0