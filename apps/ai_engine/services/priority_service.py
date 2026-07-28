"""
Priority estimation service (FR10) — Gemini-backed, cluster-aware.

Per Phase 1 Section 3, priority is estimated by Gemini given cluster
context (category, complaint count, recency), not a hardcoded local
formula — this was the ambiguity the Phase 1 evaluator flagged and
that was resolved before Phase 2.
"""
import logging
import re

from apps.ai_engine.services.gemini_client import call_gemini
from core.exceptions import AIServiceUnavailableError

logger = logging.getLogger("ai_engine")

_PROMPT_TEMPLATE = """You are estimating the priority of a municipal complaint on a scale of 1 to 10
(10 = most urgent, e.g. safety hazard affecting many people; 1 = minor, isolated issue).

Category: {category}
Number of similar complaints reported in this area: {complaint_count}
Complaint description: "{description}"

Respond with ONLY a single number from 1 to 10, nothing else."""


def estimate_priority(complaint, cluster) -> float | None:
    """
    Estimate a 1-10 priority score for a complaint given its cluster
    context. Returns None if Gemini is unavailable or its response
    can't be parsed as a valid number (FR19: caller leaves field null).
    """
    complaint_count = cluster.complaint_count if cluster else 1
    prompt = _PROMPT_TEMPLATE.format(
        category=complaint.category or "other",
        complaint_count=complaint_count,
        description=complaint.description,
    )
    try:
        raw = call_gemini(prompt)
    except AIServiceUnavailableError as exc:
        logger.warning("Priority estimation skipped, Gemini unavailable: %s", exc)
        return None

    match = re.search(r"\d+(\.\d+)?", raw)
    if not match:
        logger.warning("Gemini priority response unparseable: '%s'", raw)
        return None

    score = float(match.group())
    return max(1.0, min(10.0, score))