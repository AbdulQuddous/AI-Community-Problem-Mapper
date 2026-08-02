"""
Complaint API views.

ComplaintViewSet handles list/retrieve/create; status update is a
separate action, not the generic update(), since only status is
authority-mutable and it requires the transactional history write
(Phase 1 NFR: Data Integrity).
"""
import logging

from django.db import transaction
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Role
from apps.accounts.permissions import IsAuthorityOrAdmin, IsOwnerOrAuthorityOrAdmin
from apps.complaints.filters import ComplaintFilter
from apps.complaints.models import Complaint, ComplaintStatusHistory
from apps.complaints.serializers import (
    ComplaintReadSerializer,
    ComplaintStatusUpdateSerializer,
    ComplaintWriteSerializer,
)

logger = logging.getLogger("complaints")


class ComplaintViewSet(viewsets.ModelViewSet):
    """
    /api/complaints/

    - list, retrieve: role-scoped (citizens see own only; FR3)
    - create: citizen submits (FR2), throttled (Phase 1 rate-limiting NFR)
    - status update: separate action, authority/admin only (FR16)
    - update/partial_update/destroy (generic): disabled — complaints
      are not directly editable by citizens post-submission (no FR
      supports it), and destructive delete is disallowed (soft-delete
      only, via admin, not exposed on this API surface at all in MVP).
    """

    permission_classes = [IsAuthenticated, IsOwnerOrAuthorityOrAdmin]
    filterset_class = ComplaintFilter
    search_fields = ["description"]
    ordering_fields = ["created_at", "priority_score"]
    http_method_names = ["get", "post", "patch", "head", "options"]  # no put/delete

    def get_queryset(self):
        """
        Row-level scoping for list/retrieve — see Phase 5 Architecture
        Discussion (2.3) for why this is required in addition to the
        object-level permission class.
        """
        user = self.request.user
        base_qs = Complaint.objects.select_related("cluster").filter(is_deleted=False)
        if user.role in (Role.AUTHORITY, Role.ADMIN):
            return base_qs
        return base_qs.filter(user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return ComplaintWriteSerializer
        return ComplaintReadSerializer

    def get_throttles(self):
        if self.action == "create":
            self.throttle_scope = "complaint_submit"
        return super().get_throttles()

    def create(self, request, *args, **kwargs):
        """
        Submit a complaint (FR2). Returns 201 immediately with the
        saved complaint — AI enrichment happens out-of-band (FR18),
        triggered by the post_save signal, not here.
        """
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        complaint = write_serializer.save()
        read_serializer = ComplaintReadSerializer(complaint)
        return Response(read_serializer.data, status=http_status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["patch"],
        url_path="status",
        permission_classes=[IsAuthenticated, IsAuthorityOrAdmin],
    )
    def update_status(self, request, pk=None):
        """
        PATCH /api/complaints/{id}/status/ (FR16, authority/admin only).

        Wrapped in an atomic transaction per Phase 1's Data Integrity
        NFR: the status change and its history row must both succeed
        or both roll back.
        """
        complaint = self.get_object()
        serializer = ComplaintStatusUpdateSerializer(complaint, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        old_status = complaint.status
        new_status = serializer.validated_data["status"]

        with transaction.atomic():
            complaint.status = new_status
            complaint.save(update_fields=["status", "updated_at"])
            ComplaintStatusHistory.objects.create(
                complaint=complaint,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user,
            )

        logger.info(
            "Complaint %s status changed %s -> %s by user_id=%s",
            complaint.id, old_status, new_status, request.user.id,
        )
        return Response(ComplaintReadSerializer(complaint).data)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ComplaintSubmitFormView(LoginRequiredMixin, TemplateView):
    """GET /complaints/submit/ — the citizen-facing submission form (FR2)."""

    template_name = "complaints/submit.html"
    login_url = "/api/auth/login/"


class PublicComplaintMapPageView(LoginRequiredMixin, TemplateView):
    """GET /complaints/map/ — the citizen-facing public map page (FR4)."""

    template_name = "complaints/public_map.html"
    login_url = "/api/auth/login/"