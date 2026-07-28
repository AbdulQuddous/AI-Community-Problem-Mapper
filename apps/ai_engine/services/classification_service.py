"""
Complaint classification service (FR7) — Gemini-backed.

Uses a constrained prompt (fixed category list, few-shot examples in
both languages) and validates the response against the model's
choices before returning, so a malformed Gemini response can never
write an invalid category to the database.
"""
import logging

from apps.ai_engine.services.gemini_client import call_gemini
from apps.complaints.models import ComplaintCategory
from core.exceptions import AIServiceUnavailableError

logger = logging.getLogger("ai_engine")

_VALID_CATEGORIES = [choice[0] for choice in ComplaintCategory.choices]

_PROMPT_TEMPLATE = """You are classifying a municipal complaint into exactly one category.

Valid categories: {categories}

Examples:
"There is garbage piled up outside my house for a week" -> garbage
"سڑک پر بہت بڑا گڑھا ہے" -> roads
"No water supply in our area for 3 days" -> water
"Sewer line is overflowing near the market" -> sewer
"بجلی نہیں آرہی پچھلے دو دن سے" -> electricity

Complaint: "{description}"

Respond with ONLY the category word, nothing else."""


def classify_complaint(description: str) -> str | None:
    """
    Classify a complaint description into one of the fixed categories.

    Returns None (not "other") if Gemini is unavailable — per FR19,
    the caller (enrichment_service) is responsible for leaving
    Complaint.category as null in that case, not defaulting to a
    guessed value.
    """
    prompt = _PROMPT_TEMPLATE.format(
        categories=", ".join(_VALID_CATEGORIES), description=description
    )
    try:
        raw = call_gemini(prompt).strip().lower()
    except AIServiceUnavailableError as exc:
        logger.warning("Classification skipped, Gemini unavailable: %s", exc)
        return None

    if raw in _VALID_CATEGORIES:
        return raw

    logger.warning("Gemini returned an unrecognized category '%s'; leaving null.", raw)
    return None