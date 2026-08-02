"""
Public (any authenticated citizen) read-only map view (FR4).

Separate from ComplaintViewSet — see Phase 8 Architecture Discussion
(2.1) for why this is its own small, auditable view rather than a
branch inside the existing viewset.
"""
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.complaints.models import Complaint
from apps.complaints.public_serializers import PublicComplaintMapSerializer


class PublicComplaintMapView(ListAPIView):
    """
    GET /api/complaints/public-map/

    Returns all active (non-deleted, non-resolved) complaints with
    only map-safe fields (see PublicComplaintMapSerializer). Any
    authenticated citizen/authority can view this — it is
    intentionally not role-restricted, since FR4 is a citizen-facing
    feature by definition, and there is no privacy reason to also
    block authority accounts from seeing it.

    No pagination: at capstone scale, returning the full active set
    lets the client render everything in one map pass (see Phase 8
    Architecture Discussion 2.3 for the scale tradeoff this accepts).
    """

    serializer_class = PublicComplaintMapSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Complaint.objects.filter(is_deleted=False).exclude(status="resolved")