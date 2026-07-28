"""
Cluster summarization service (FR12) — Gemini-backed.

Only called by enrichment_service when a cluster is newly created or
crosses a size threshold (see Phase 6 Architecture Discussion 2.6),
to avoid an expensive Gemini call on every single complaint added to
an already-summarized cluster.
"""
import logging

from apps.ai_engine.services.gemini_client import call_gemini
from core.exceptions import AIServiceUnavailableError

logger = logging.getLogger("ai_engine")

_MAX_DESCRIPTIONS_IN_PROMPT = 10

_PROMPT_TEMPLATE = """Summarize the following municipal complaints, which have been grouped
together as reports of the same issue in one area. Write 2-4 sentences describing the
common issue, its approximate scale, and severity. Do not list every complaint individually.

Category: {category}
Number of complaints in this group: {complaint_count}

Complaints:
{descriptions}

Summary:"""


def summarize_cluster(cluster) -> str | None:
    """
    Generate a human-readable summary for a cluster/hotspot.

    Returns None if Gemini is unavailable — caller (enrichment_service)
    leaves Cluster.summary_text at its previous value (or null) rather
    than overwriting it with nothing (FR19).
    """
    from apps.complaints.models import Complaint

    descriptions = list(
        Complaint.objects.filter(cluster=cluster, is_deleted=False)
        .order_by("-created_at")
        .values_list("description", flat=True)[:_MAX_DESCRIPTIONS_IN_PROMPT]
    )
    if not descriptions:
        return None

    prompt = _PROMPT_TEMPLATE.format(
        category=cluster.category,
        complaint_count=cluster.complaint_count,
        descriptions="\n".join(f"- {d}" for d in descriptions),
    )
    try:
        return call_gemini(prompt)
    except AIServiceUnavailableError as exc:
        logger.warning("Summarization skipped, Gemini unavailable: %s", exc)
        return None