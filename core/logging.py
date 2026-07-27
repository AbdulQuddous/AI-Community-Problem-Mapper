"""
Centralized logging configuration.

Referenced from config/settings.py. Kept in core/ rather than inline
in settings.py so the AI pipeline (Phase 6) and API layers can share
one consistent logging setup, per Phase 1's Observability NFR
(structured logging including explicit Gemini fallback logging).
"""

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        # Dedicated logger namespace for AI pipeline stages (Phase 6),
        # so Gemini failures/fallbacks (FR19) are clearly traceable.
        "ai_engine": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "complaints": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}