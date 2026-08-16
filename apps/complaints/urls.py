"""URL routing for the complaints app, mounted at /api/complaints/."""
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.complaints.manage_views import ComplaintManageListView
from apps.complaints.public_views import PublicComplaintMapView
from apps.complaints.views import ComplaintViewSet

router = DefaultRouter()
router.register(r"", ComplaintViewSet, basename="complaint")

urlpatterns = [
    # Registered before the router's catch-all detail route (/<pk>/)
    # to avoid DRF interpreting these fixed segments as UUID lookups.
    path("public-map/", PublicComplaintMapView.as_view(), name="complaint-public-map"),
    path("manage/", ComplaintManageListView.as_view(), name="complaint-manage-list"),
] + router.urls