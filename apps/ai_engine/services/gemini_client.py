"""
Single chokepoint for all Gemini API calls.

Every Gemini-calling service (classification, priority, summarization)
routes through call_gemini() so failure handling is written exactly
once, satisfying FR19: a Gemini failure must never crash the
enrichment pipeline, only cause that one field to stay null.

Uses the google-genai SDK (the modern replacement for the deprecated
google-generativeai package). This SDK uses a simple, direct API-key
client with no gRPC/ADC credential resolution ambiguity — it was
adopted specifically because the old SDK intermittently authenticated
via an unrelated ambient credential path on this project's dev
machine instead of honoring the explicit API key.
"""
import logging

from google import genai
from django.conf import settings

from core.exceptions import AIServiceUnavailableError

logger = logging.getLogger("ai_engine")

_client = None


def _get_client():
    """Lazily construct the genai Client exactly once per process."""
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise AIServiceUnavailableError("GEMINI_API_KEY is not set.")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def call_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the raw text response.

    Raises:
        AIServiceUnavailableError: on any failure (missing key, network
            error, API error, empty response). Callers must catch this
            and apply the FR19 fallback (leave the relevant field null)
            rather than letting it propagate to the enrichment thread's
            caller.
    """
    try:
        client = _get_client()
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents=prompt,
        )
        text = (response.text or "").strip()
        if not text:
            raise AIServiceUnavailableError("Gemini returned an empty response.")
        return text
    except AIServiceUnavailableError:
        raise
    except Exception as exc:  # noqa: BLE001 — intentionally broad, see docstring
        logger.warning("Gemini API call failed: %s", exc)
        raise AIServiceUnavailableError(str(exc)) from exc