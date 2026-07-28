"""
Entry point for asynchronous complaint enrichment.

This module is intentionally a real, honest stub for Phase 5: it
performs the actual signal->thread->save round trip so that behavior
is testable now, but does not yet call Sentence Transformers, DBSCAN,
or Gemini — those are wired in Phase 6 inside this same function,
without changing its signature or call site (apps/complaints/signals.py).

Design contract this function must uphold (per FR18/FR19):
  - Must never raise an exception that escapes to the caller thread
    unhandled (would silently kill the background thread with no
    record).
  - Must leave AI fields as their nullable defaults if anything fails,
    never leave the Complaint row in a partially-corrupt state.
"""
import logging

logger = logging.getLogger("ai_engine")


def enrich_complaint(complaint_id: str) -> None:
    """
    Run AI enrichment for a single complaint, out-of-band from the
    request/response cycle.

    Args:
        complaint_id: UUID (as string) of the Complaint to enrich.
            Passed as a string, not a model instance, because this
            function runs in a background thread and must re-fetch
            the row itself rather than share an ORM object across
            threads.

    Phase 6 will implement, in order, inside this function:
        1. Fetch the Complaint by id.
        2. Detect language (FR5).
        3. Generate embedding via Sentence Transformers (FR6).
        4. Run duplicate detection via cosine similarity (FR8).
           If a duplicate is found, set duplicate_of and return early.
        5. Classify category via Gemini (FR7).
        6. Run DBSCAN clustering, inline, bounded to recent complaints
           (FR9, FR9A).
        7. Estimate priority via Gemini (FR10).
        8. If cluster is new/updated, generate Gemini summary (FR12).
        9. Save all fields in a single update, wrapped so any Gemini
           failure at steps 5/7/8 logs and leaves that field null
           (FR19) without blocking steps that don't depend on it.
    """
    from apps.complaints.models import Complaint  # local import: avoid
    # app-loading-order issues, since this module is imported from
    # complaints/signals.py during app startup.

    try:
        complaint = Complaint.objects.get(id=complaint_id)
    except Complaint.DoesNotExist:
        logger.error("Enrichment skipped: Complaint %s not found.", complaint_id)
        return

    logger.info(
        "Enrichment stub invoked for complaint_id=%s (Phase 6 will implement "
        "embedding/classification/clustering/priority/summary here).",
        complaint.id,
    )
    # Intentionally no-op beyond logging in Phase 5. All AI fields
    # remain at their nullable defaults, which is correct and expected
    # per FR19 until Phase 6 lands.