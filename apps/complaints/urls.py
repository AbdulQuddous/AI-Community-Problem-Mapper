"""URL routing for the complaints app, mounted at /api/complaints/."""
from rest_framework.routers import DefaultRouter

from apps.complaints.views import ComplaintViewSet

router = DefaultRouter()
router.register(r"", ComplaintViewSet, basename="complaint")

urlpatterns = router.urls