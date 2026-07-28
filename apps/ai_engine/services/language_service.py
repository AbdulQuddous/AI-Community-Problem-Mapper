"""
Language detection service (FR5).

Uses langdetect rather than a Gemini call — this is a cheap, local,
deterministic classification task that doesn't need an LLM, keeping
it off Gemini's critical path per the tradeoff noted in Phase 6
Architecture Discussion (2.1: Gemini is reserved for classification,
priority, and summarization only).
"""
import logging

from langdetect import LangDetectException, detect

from apps.complaints.models import ComplaintLanguage

logger = logging.getLogger("ai_engine")

_LANGDETECT_TO_MODEL = {
    "ur": ComplaintLanguage.URDU,
    "en": ComplaintLanguage.ENGLISH,
}


def detect_language(text: str) -> str:
    """
    Detect whether the complaint text is Urdu or English.

    Returns ComplaintLanguage.UNKNOWN if detection fails or the
    detected language isn't one of the two the system supports —
    this is a local, non-Gemini step, so it does not participate in
    the FR19 fallback contract; failure here simply means "unknown",
    not "pipeline degraded."
    """
    try:
        detected = detect(text)
        return _LANGDETECT_TO_MODEL.get(detected, ComplaintLanguage.UNKNOWN)
    except LangDetectException as exc:
        logger.info("Language detection failed, defaulting to unknown: %s", exc)
        return ComplaintLanguage.UNKNOWN