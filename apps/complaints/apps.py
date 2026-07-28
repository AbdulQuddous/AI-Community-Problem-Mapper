from django.apps import AppConfig


class ComplaintsConfig(AppConfig):
    """
    App config for complaint CRUD and status history.

    ready() imports signals.py so the post_save receiver registers
    at app startup — this is the standard, documented Django pattern
    for signal registration, avoiding import-order bugs.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.complaints"

    def ready(self) -> None:
        import apps.complaints.signals  # noqa: F401