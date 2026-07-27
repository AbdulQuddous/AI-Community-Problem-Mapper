"""
Shared abstract base model used across all domain apps.

Provides UUID primary keys, audit timestamps, and soft-delete support
so that every domain model gets these behaviors for free without
duplicating fields across apps.
"""
import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing common fields for all domain entities.

    Fields:
        id: UUID primary key (avoids sequential-ID enumeration, safer for
            a public-facing citizen API).
        created_at: Set once on creation.
        updated_at: Refreshed on every save.
        is_deleted: Soft-delete flag. Citizen complaints should not be
            hard-deleted (audit/trust requirement from Phase 1 NFRs).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]