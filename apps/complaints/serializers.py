"""
Serializers for the Complaint module.

Two serializers are deliberately separate: ComplaintWriteSerializer
(citizen submission, narrow field set) and ComplaintReadSerializer
(full representation including AI fields, used for list/retrieve).
Collapsing these into one serializer would let a citizen see or
attempt to set AI-derived fields they should never touch directly.
"""
import logging

from rest_framework import serializers

from apps.ai_engine.models import Cluster
from apps.complaints.models import Complaint, ComplaintStatusHistory

logger = logging.getLogger("complaints")

MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]


class ClusterSummarySerializer(serializers.ModelSerializer):
    """Minimal nested representation of a Complaint's cluster, if assigned."""

    class Meta:
        model = Cluster
        fields = ["id", "is_hotspot", "complaint_count", "priority_score"]
        read_only_fields = fields


class ComplaintWriteSerializer(serializers.ModelSerializer):
    """
    Used for POST /api/complaints/ (citizen submission, FR2).

    Only accepts citizen-controllable fields. category, priority_score,
    embedding, cluster, duplicate_of, status are never accepted here —
    they are either system-managed or AI-populated (FR18/FR19).
    """

    class Meta:
        model = Complaint
        fields = ["id", "description", "latitude", "longitude", "image", "language"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "language": {"required": False},
        }

    def validate_description(self, value: str) -> str:
        """Ensure the complaint has meaningful content (FR2)."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Description must be at least 10 characters."
            )
        return value.strip()

    def validate_image(self, value):
        """
        Enforce file type/size limits — Phase 1 risk mitigation for
        image upload abuse.
        """
        if value is None:
            return value
        if value.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image must be smaller than {MAX_IMAGE_SIZE_MB}MB."
            )
        content_type = getattr(value, "content_type", None)
        if content_type not in ALLOWED_IMAGE_TYPES:
            raise serializers.ValidationError(
                f"Unsupported image type: {content_type}. "
                f"Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}."
            )
        return value

    def validate(self, attrs: dict) -> dict:
        """Validate latitude/longitude are within plausible real-world bounds."""
        lat = attrs.get("latitude")
        lon = attrs.get("longitude")
        if lat is not None and not (-90 <= lat <= 90):
            raise serializers.ValidationError({"latitude": "Must be between -90 and 90."})
        if lon is not None and not (-180 <= lon <= 180):
            raise serializers.ValidationError({"longitude": "Must be between -180 and 180."})
        return attrs

    def create(self, validated_data: dict) -> Complaint:
        """Attach the requesting user; language defaults to unknown until
        Phase 6's language detection step runs."""
        validated_data["user"] = self.context["request"].user
        complaint = Complaint.objects.create(**validated_data)
        logger.info(
            "Complaint created: id=%s user_id=%s", complaint.id, complaint.user_id
        )
        return complaint


class ComplaintReadSerializer(serializers.ModelSerializer):
    """
    Used for GET (list/retrieve). Includes AI-derived fields as
    read-only, and a nested cluster summary for dashboard/authority
    consumption (FR13, FR14).
    """

    cluster = ClusterSummarySerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "id", "user", "description", "language", "category", "status",
            "priority_score", "cluster", "duplicate_of", "latitude", "longitude",
            "image", "created_at", "updated_at",
        ]
        read_only_fields = fields


class ComplaintStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Used for PATCH /api/complaints/{id}/status/ (FR16, authority-only).

    Deliberately its own serializer rather than reusing
    ComplaintReadSerializer with partial=True — status transitions
    need their own validation (no arbitrary jump to any status) and
    must write a ComplaintStatusHistory row, which a generic
    serializer update() wouldn't know to do.
    """

    class Meta:
        model = Complaint
        fields = ["status"]

    def validate_status(self, value: str) -> str:
        valid_statuses = [choice[0] for choice in Complaint._meta.get_field("status").choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status: {value}")
        return value