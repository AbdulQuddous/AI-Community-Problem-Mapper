"""
Authority-facing complaint management: list + status toggle.

Reuses ComplaintViewSet's existing `update_status` action (Phase 5)
for the actual status change — this module only adds the grouped
list view and the page shell, per the "avoid duplicated code"
principle.
"""
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAuthorityOrAdmin
from apps.complaints.filters import ComplaintFilter
from apps.complaints.manage_serializers import ComplaintManageSerializer
from apps.complaints.models import Complaint


class ComplaintManageListView(ListAPIView):
    """
    GET /api/complaints/manage/

    Returns only "main" complaints (duplicate_of is null) with their
    AI-detected duplicates nested inline. Supports the same
    category/status/date filters as the regular complaint list and
    dashboard stats (ComplaintFilter, Phase 5/7), applied to the main
    complaint's own fields.
    """

    serializer_class = ComplaintManageSerializer
    permission_classes = [IsAuthenticated, IsAuthorityOrAdmin]
    filterset_class = ComplaintFilter

    def get_queryset(self):
        return (
            Complaint.objects.filter(is_deleted=False, duplicate_of__isnull=True)
            .select_related("cluster")
            .prefetch_related("duplicates")
            .order_by("-created_at")
        )


class ComplaintManagePageView(TemplateView):
    """
    GET /complaints/manage/ — HTML shell. No LoginRequiredMixin, same
    reasoning as DashboardOverviewView (Phase 7 fix): auth is JWT in
    localStorage, not Django sessions, so gating happens client-side
    in manage.js plus server-side on the actual API calls.
    """

    template_name = "complaints/manage.html"