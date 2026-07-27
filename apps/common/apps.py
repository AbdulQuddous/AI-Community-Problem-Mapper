from django.apps import AppConfig


class CommonConfig(AppConfig):
    """App config for the shared abstract-model app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"