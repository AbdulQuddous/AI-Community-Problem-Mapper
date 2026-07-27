"""
Complaint and ComplaintStatusHistory models.

Design note: nearly every AI-derived field on Complaint (embedding,
category, priority_score, cluster) is nullable. This is intentional,
not an oversight — per FR18/FR19, a complaint is saved and returned
to the citizen immediately, before any AI enrichment has run, and
must remain fully usable even if Gemini enrichment never completes.
"""
from django.conf import settings
from django.db import models

from apps.ai_engine.models import Cluster
from apps.common.models import BaseModel


class ComplaintCategory(models.TextChoices):
    """Fixed category list, locked in Phase 1 Section 9 assumptions."""

    GARBAGE = "garbage", "Garbage"
    ROADS = "roads", "Broken Roads"
    WATER = "water", "Water Shortage"
    SEWER = "sewer", "Sewer Problem"
    ELECTRICITY = "electricity", "Electricity Outage"
    STREETLIGHTS = "streetlights", "Street Lights"
    ILLEGAL_DUMPING = "illegal_dumping", "Illegal Dumping"
    CLEANLINESS = "cleanliness", "Public Cleanliness"
    OTHER = "other", "Other"


class ComplaintStatus(models.TextChoices):
    """Status lifecycle referenced in FR16."""

    RECEIVED = "received", "Received"
    IN_REVIEW = "in_review", "In Review"
    IN_PROGRESS = "in_progress", "In Progress"
    RESOLVED = "resolved", "Resolved"


class ComplaintLanguage(models.TextChoices):
    """Detected language, per FR5."""

    URDU = "ur", "Urdu"
    ENGLISH = "en", "English"
    UNKNOWN = "unknown", "Unknown"


class Complaint(BaseModel):
    """
    A citizen-submitted complaint and its AI enrichment state.

    AI fields are populated asynchronously (see Phase 2 sequence
    diagram, section 5.1) and are therefore nullable:
        - embedding: Sentence Transformer vector (FR6).
        - category: Gemini classification result (FR7).
        - priority_score: Gemini priority estimate (FR10).
        - cluster: DBSCAN cluster assignment (FR9).
        - duplicate_of: set by the duplicate-detection service (FR8)
          when a near-duplicate is found; the original complaint is
          preserved and linked rather than the new one being dropped.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="complaints",
    )
    description = models.TextField()
    language = models.CharField(
        max_length=10,
        choices=ComplaintLanguage.choices,
        default=ComplaintLanguage.UNKNOWN,
    )
    category = models.CharField(
        max_length=30,
        choices=ComplaintCategory.choices,
        null=True,
        blank=True,
        help_text="Null until Gemini classification completes (FR19).",
    )
    status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.RECEIVED,
    )
    priority_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Null until Gemini priority estimation completes (FR19).",
    )
    embedding = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Sentence Transformer embedding vector, stored as a JSON "
            "array of floats. Not pgvector in MVP — see Phase 2 tradeoffs."
        ),
    )
    cluster = models.ForeignKey(
        Cluster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="complaints",
    )
    duplicate_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="duplicates",
        help_text="Set when duplicate-detection links this to an existing complaint.",
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(
        upload_to="complaints/%Y/%m/",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "complaints_complaint"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self) -> str:
        return f"Complaint({self.id}) - {self.category or 'uncategorized'}"


class ComplaintStatusHistory(BaseModel):
    """
    Audit trail of status transitions for a complaint (FR20).

    Written inside the same DB transaction as the status update on
    Complaint (see Phase 2 sequence diagram, section 5.2) so the two
    never go out of sync.
    """

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name="status_history",
    )
    old_status = models.CharField(max_length=20, choices=ComplaintStatus.choices)
    new_status = models.CharField(max_length=20, choices=ComplaintStatus.choices)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="status_changes",
    )

    class Meta:
        db_table = "complaints_status_history"

    def __str__(self) -> str:
        return f"{self.complaint_id}: {self.old_status} -> {self.new_status}"