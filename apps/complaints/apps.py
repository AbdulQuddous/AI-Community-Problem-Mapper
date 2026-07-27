from django.apps import AppConfig


class ComplaintsConfig(AppConfig):
    """
    App config for complaint CRUD and status history.

    ready() will register the post_save signal (FR18) in Phase 5,
    once the complaint views/services exist to hand enrichment off to.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.complaints"