"""
Serializer for the citizen-facing public map endpoint (FR4).

Deliberately excludes: user, description (full text), image, and any
other field that could identify the reporter or over-expose detail
better suited to the authority dashboard. See Phase 8 Architecture
Discussion (2.1) for the privacy boundary this enforces.
"""
from rest_framework import serializers

from apps.complaints.models import Complaint


class PublicComplaintMapSerializer(serializers.ModelSerializer):
    """
    Minimal, privacy-safe representation of a complaint for the
    public map. No reporter identity, no exact description text
    (a short category label is sufficient for a map pin).
    """

    class Meta:
        model = Complaint
        fields = ["id", "category", "status", "latitude", "longitude", "created_at"]
        read_only_fields = fields