from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """App config for read-only aggregation/reporting views."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"