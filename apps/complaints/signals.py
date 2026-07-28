"""
Signal wiring for out-of-band AI enrichment (FR18).

A post_save signal, fired only on creation (not on every update —
otherwise every status change or admin edit would re-trigger the full
AI pipeline), hands off to a background thread. No message broker
involved, per Phase 1's revised constraints.
"""
import logging
import threading

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.ai_engine.services.enrichment_service import enrich_complaint
from apps.complaints.models import Complaint

logger = logging.getLogger("complaints")


@receiver(post_save, sender=Complaint)
def trigger_enrichment_on_create(sender, instance: Complaint, created: bool, **kwargs) -> None:
    """
    Fires only when a new Complaint row is first created.

    Runs enrichment in a daemon thread so the request/response cycle
    (already completed by the time this fires, since post_save runs
    after the DB write) is never blocked. Any exception inside the
    thread is caught by enrich_complaint's own error handling
    (Phase 6) — this receiver itself stays minimal by design.
    """
    if not created:
        return

    thread = threading.Thread(
        target=enrich_complaint,
        args=(str(instance.id),),
        daemon=True,
    )
    thread.start()
    logger.info("Enrichment thread started for complaint_id=%s", instance.id)