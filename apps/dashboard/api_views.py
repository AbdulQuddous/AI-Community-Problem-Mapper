"""
JSON API views for the dashboard, consumed by dashboard.js/map.js via
fetch. No models live here — every view queries apps.complaints and
apps.ai_engine, per Phase 7 Architecture Discussion (2.1).
"""
import logging
from datetime import timedelta

from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAuthorityOrAdmin
from apps.ai_engine.models import Cluster
from apps.complaints.filters import ComplaintFilter
from apps.complaints.models import Complaint
from apps.dashboard.serializers import ClusterDetailSerializer, ClusterHotspotSerializer

logger = logging.getLogger("django")

TREND_WINDOW_DAYS = 30


class DashboardStatsView(APIView):
    """
    GET /api/dashboard/stats/ (FR13, FR15)

    Returns category breakdown, status breakdown, and a daily trend
    for the last 30 days — in one response, per Phase 7 Architecture
    Discussion (2.3). Accepts the same filters as ComplaintFilter
    (category, status, date_from, date_to) via query params, applied
    before aggregation (2.5).
    """

    permission_classes = [IsAuthenticated, IsAuthorityOrAdmin]

    def get(self, request):
        base_qs = Complaint.objects.filter(is_deleted=False)
        filtered_qs = ComplaintFilter(request.query_params, queryset=base_qs).qs

        category_breakdown = list(
            filtered_qs.exclude(category__isnull=True)
            .values("category")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        status_breakdown = list(
            filtered_qs.values("status").annotate(count=Count("id")).order_by("status")
        )

        trend_start = timezone.now() - timedelta(days=TREND_WINDOW_DAYS)
        daily_trend = list(
            filtered_qs.filter(created_at__gte=trend_start)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        summary = {
            "total_complaints": filtered_qs.count(),
            "unresolved_count": filtered_qs.exclude(status="resolved").count(),
            "average_priority": filtered_qs.exclude(priority_score__isnull=True).aggregate(
                avg=Avg("priority_score")
            )["avg"],
        }

        return Response({
            "summary": summary,
            "category_breakdown": category_breakdown,
            "status_breakdown": status_breakdown,
            "daily_trend": daily_trend,
        })


class HotspotListView(ListAPIView):
    """
    GET /api/dashboard/hotspots/ (FR11, FR14)

    Direct read of persisted Cluster rows flagged as hotspots — does
    not recompute clustering, per Phase 7 Architecture Discussion (2.4).
    """

    serializer_class = ClusterHotspotSerializer
    permission_classes = [IsAuthenticated, IsAuthorityOrAdmin]

    def get_queryset(self):
        return Cluster.objects.filter(is_hotspot=True, is_deleted=False).order_by(
            "-complaint_count"
        )


class ClusterDetailView(RetrieveAPIView):
    """
    GET /api/dashboard/clusters/{id}/ (US4)

    Returns the full cluster detail including the Gemini-generated
    summary, for the authority's cluster drill-down view.
    """

    serializer_class = ClusterDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorityOrAdmin]
    queryset = Cluster.objects.filter(is_deleted=False)