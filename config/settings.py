"""
Django settings for the AI Powered Community Problem Mapper.

Single-file settings, environment-variable driven via django-environ.
Deliberately not split into base/dev/prod modules — see Phase 3
Architecture Discussion (section 2.1) for rationale. All secrets and
environment-specific values live in .env (gitignored); .env.example
documents every required variable.
"""
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    # Local apps
    "apps.common",
    "apps.accounts",
    "apps.complaints",
    "apps.ai_engine",
    "apps.dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Database ---------------------------------------------------------
# PostgreSQL, connected to a locally installed instance (no Docker —
# see Phase 3 section 2.2). Setup instructions provided in Phase 10 README.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

# --- Custom user model (Phase 2 / Phase 4) -----------------------------
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ---------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        # Applied to the complaint submission endpoint (Phase 5) to
        # satisfy Phase 1's rate-limiting security requirement.
        "complaint_submit": "10/hour",
    },
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
}

# --- SimpleJWT (Phase 4) ------------------------------------------------
from datetime import timedelta  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("ACCESS_TOKEN_LIFETIME_MINUTES", default=60)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env.int("REFRESH_TOKEN_LIFETIME_DAYS", default=7)
    ),
    "ROTATE_REFRESH_TOKENS": True,
}

# --- CORS ----------------------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# --- Gemini API (used in ai_engine services, Phase 6) --------------------
GEMINI_API_KEY = env("GEMINI_API_KEY", default="")
# --- AI Pipeline configuration (Phase 6) ---------------------------------
SENTENCE_TRANSFORMER_MODEL = env(
    "SENTENCE_TRANSFORMER_MODEL", default="paraphrase-multilingual-MiniLM-L12-v2"
)
GEMINI_MODEL_NAME = env("GEMINI_MODEL_NAME", default="gemini-1.5-flash")

# Duplicate detection (FR8) — geo-bounded cosine similarity
DUPLICATE_SIMILARITY_THRESHOLD = env.float("DUPLICATE_SIMILARITY_THRESHOLD", default=0.85)
DUPLICATE_GEO_RADIUS_KM = env.float("DUPLICATE_GEO_RADIUS_KM", default=0.5)

# Clustering / hotspot detection (FR9, FR9A, FR11)
CLUSTERING_WINDOW_DAYS = env.int("CLUSTERING_WINDOW_DAYS", default=90)
DBSCAN_EPS_KM = env.float("DBSCAN_EPS_KM", default=0.3)
DBSCAN_MIN_SAMPLES = env.int("DBSCAN_MIN_SAMPLES", default=3)
HOTSPOT_MIN_COMPLAINTS = env.int("HOTSPOT_MIN_COMPLAINTS", default=5)

# Cluster centroid matching — how close a new cluster's centroid must be
# to an existing Cluster row's centroid to be considered "the same" hotspot
CLUSTER_MATCH_RADIUS_KM = env.float("CLUSTER_MATCH_RADIUS_KM", default=0.4)

# Summary regeneration threshold — only call Gemini for a new summary
# when the cluster crosses this size or was just created (see 2.6)
SUMMARY_REGEN_STEP = env.int("SUMMARY_REGEN_STEP", default=3)

# --- Logging (delegates to core/logging.py) ------------------------------
from core.logging import LOGGING_CONFIG, LOGGING

LOGIN_URL = "/api/auth/login/"
