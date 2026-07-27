"""
Django admin registration for User.

Municipal authority/admin accounts are provisioned here manually
(via createsuperuser or admin panel), not through the public
registration endpoint — see Phase 4 Architecture Discussion (2.3).
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Extends Django's built-in UserAdmin to surface the role field."""

    fieldsets = UserAdmin.fieldsets + (
        ("Role & Contact", {"fields": ("role", "phone_number")}),
    )
    list_display = ["username", "email", "role", "is_active", "date_joined"]
    list_filter = UserAdmin.list_filter + ("role",)