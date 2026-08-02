"""URL routing for the complaints app, mounted at /api/complaints/."""
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.complaints.public_views import PublicComplaintMapView
from apps.complaints.views import ComplaintViewSet

router = DefaultRouter()
router.register(r"", ComplaintViewSet, basename="complaint")

urlpatterns = [
    # Must be registered before the router's catch-all detail route
    # (/<pk>/) to avoid DRF interpreting "public-map" as a UUID lookup.
    path("public-map/", PublicComplaintMapView.as_view(), name="complaint-public-map"),
] + router.urls