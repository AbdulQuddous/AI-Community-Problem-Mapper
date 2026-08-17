"""
Serializers for the Complaint module.
"""
import logging

from langdetect import LangDetectException, detect
from rest_framework import serializers

from apps.ai_engine.models import Cluster
from apps.complaints.models import Complaint, ComplaintStatusHistory

logger = logging.getLogger("complaints")

MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]


class ClusterSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ["id", "is_hotspot", "complaint_count", "priority_score"]
        read_only_fields = fields


class ComplaintWriteSerializer(serializers.ModelSerializer):
    """
    Used for POST /api/complaints/ (citizen submission, FR2).

    The system has been scoped to English-only submissions (a
    deliberate reduction from the original Urdu/English dual-language
    requirement) to avoid the reliability problems of cross-script/
    cross-lingual embedding similarity and classification — see
    project notes on duplicate_service.py for the history here.
    Non-English text is rejected at submission time with a clear
    error, rather than silently mishandled downstream in enrichment.
    """

    class Meta:
        model = Complaint
        fields = ["id", "description", "latitude", "longitude", "image", "language"]
        read_only_fields = ["id", "language"]

    def validate_description(self, value: str) -> str:
        """Ensure the complaint has meaningful content (FR2) and is in English."""
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must be at least 10 characters."
            )

        try:
            detected = detect(value)
        except LangDetectException:
            detected = None

        if detected != "en":
            raise serializers.ValidationError(
                "Please submit your complaint in English. "
                "The system currently only supports English descriptions."
            )
        return value

    def validate_image(self, value):
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
        lat = attrs.get("latitude")
        lon = attrs.get("longitude")
        if lat is not None and not (-90 <= lat <= 90):
            raise serializers.ValidationError({"latitude": "Must be between -90 and 90."})
        if lon is not None and not (-180 <= lon <= 180):
            raise serializers.ValidationError({"longitude": "Must be between -180 and 180."})
        return attrs

    def create(self, validated_data: dict) -> Complaint:
        validated_data["user"] = self.context["request"].user
        validated_data["language"] = "en"  # enforced at validation, so this is always safe now
        complaint = Complaint.objects.create(**validated_data)
        logger.info(
            "Complaint created: id=%s user_id=%s", complaint.id, complaint.user_id
        )
        return complaint


class ComplaintReadSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Complaint
        fields = ["status"]

    def validate_status(self, value: str) -> str:
        valid_statuses = [choice[0] for choice in Complaint._meta.get_field("status").choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status: {value}")
        return value