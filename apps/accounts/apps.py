from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """App config for authentication and the custom User model."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"