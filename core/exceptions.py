"""
Shared exception types and a custom DRF exception handler.

Centralizing error handling here (rather than per-view try/except)
satisfies the master prompt's "handle errors gracefully" and "avoid
duplicated code" requirements.
"""
import logging

from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("django")


class AIServiceUnavailableError(Exception):
    """
    Raised internally by ai_engine services (Phase 6) when Gemini API
    calls fail. Caught by the calling service, not surfaced to the
    citizen — per FR19, the complaint must still save successfully.
    """


class DuplicateComplaintDetected(Exception):
    """
    Raised internally by the duplicate-detection service (Phase 6)
    to short-circuit further enrichment once a complaint is linked
    to an existing one via duplicate_of.
    """


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler to add consistent logging
    for every unhandled API exception, satisfying the Observability NFR.
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        logger.warning(
            "API exception: %s | view=%s | detail=%s",
            exc.__class__.__name__,
            context.get("view"),
            response.data,
        )
    else:
        logger.error(
            "Unhandled exception: %s | view=%s",
            exc.__class__.__name__,
            context.get("view"),
            exc_info=True,
        )

    return response