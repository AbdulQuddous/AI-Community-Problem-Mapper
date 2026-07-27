import logging.config

LOGGING_CONFIG = "logging.config.dictConfig"

LOGGING = {
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
