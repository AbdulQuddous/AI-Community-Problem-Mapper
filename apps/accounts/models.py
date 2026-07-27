"""
Custom User model for the Community Problem Mapper.

We extend AbstractUser rather than building a fully custom user model
from scratch: it's the lowest-risk path to add a `role` field while
keeping Django's built-in auth machinery (password hashing, admin
integration) intact, which matters for a 2-week timeline.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """Defines the three user roles established in Phase 1 (Primary Users)."""

    CITIZEN = "citizen", "Citizen"
    AUTHORITY = "authority", "Municipal Authority"
    ADMIN = "admin", "City Administrator"


class User(AbstractUser):
    """
    Custom user model with a role field.

    Phase 1 assumption: citizens must register/log in to submit a
    complaint (no anonymous submission), so every Complaint.user FK
    is non-nullable and always resolves to a real, authenticated User.
    """

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CITIZEN,
        help_text="Determines dashboard/API access level.",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Optional; used for contact/notification purposes.",
    )

    class Meta:
        db_table = "accounts_user"

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"