"""
Serializers for the authority-facing complaint management page
(/complaints/manage/). Groups complaints under their AI-detected
"main" complaint, per Phase 6's duplicate_of linkage — no new
grouping logic is introduced here, this only surfaces what the
enrichment pipeline already determined.
"""
from rest_framework import serializers

from apps.complaints.models import Complaint


class DuplicateComplaintSerializer(serializers.ModelSerializer):
    """
    Lightweight representation of a complaint nested under its main
    complaint. Deliberately has no `duplicates` field of its own —
    duplicate_of chains are always one level deep (a duplicate never
    points to another duplicate; find_duplicate in Phase 6 only
    matches against non-resolved complaints and stores a direct
    reference), so no recursion is needed here.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Complaint
        fields = ["id", "description", "status", "user", "created_at"]
        read_only_fields = fields


class ComplaintManageSerializer(serializers.ModelSerializer):
    """
    Main complaint representation for the manage page, with its
    AI-linked duplicates nested inline, plus the cluster's AI-written
    summary (if one exists) so authority can see the hotspot's
    overview without opening the dashboard separately.
    """

    duplicates = DuplicateComplaintSerializer(many=True, read_only=True)
    duplicate_count = serializers.IntegerField(source="duplicates.count", read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    cluster_summary = serializers.CharField(source="cluster.summary_text", read_only=True, default=None)
    is_hotspot = serializers.BooleanField(source="cluster.is_hotspot", read_only=True, default=False)

    class Meta:
        model = Complaint
        fields = [
            "id", "description", "category", "status", "priority_score",
            "latitude", "longitude", "user", "created_at",
            "duplicate_count", "duplicates", "cluster_summary", "is_hotspot",
        ]
        read_only_fields = fields