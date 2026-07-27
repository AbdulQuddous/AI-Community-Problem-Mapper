from django.apps import AppConfig


class AiEngineConfig(AppConfig):
    """App config for the Cluster model and AI service modules."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai_engine"