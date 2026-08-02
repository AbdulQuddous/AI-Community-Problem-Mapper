"""
Serializers for dashboard read endpoints.

Kept separate from apps/complaints/serializers.py — the dashboard
needs different, aggregation-shaped output (counts, centroids) rather
than individual complaint representations.
"""
from rest_framework import serializers

from apps.ai_engine.models import Cluster


class ClusterHotspotSerializer(serializers.ModelSerializer):
    """
    Used for GET /api/dashboard/hotspots/ (FR11, FR14) — map marker
    data plus enough info for a popup/info-window without a second
    request.
    """

    class Meta:
        model = Cluster
        fields = [
            "id", "category", "centroid_latitude", "centroid_longitude",
            "complaint_count", "priority_score", "is_hotspot", "updated_at",
        ]
        read_only_fields = fields


class ClusterDetailSerializer(serializers.ModelSerializer):
    """Used for GET /api/dashboard/clusters/{id}/ (US4) — includes the
    Gemini summary, which the list/hotspot view omits to keep payload small."""

    class Meta:
        model = Cluster
        fields = [
            "id", "category", "centroid_latitude", "centroid_longitude",
            "complaint_count", "priority_score", "summary_text",
            "is_hotspot", "created_at", "updated_at",
        ]
        read_only_fields = fields