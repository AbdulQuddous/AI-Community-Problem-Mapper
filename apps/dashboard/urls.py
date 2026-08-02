"""URL routing for the dashboard app: API endpoints + the template shell."""
from django.urls import path

from apps.dashboard.api_views import ClusterDetailView, DashboardStatsView, HotspotListView
from apps.dashboard.views import DashboardOverviewView

urlpatterns = [
    path("stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("hotspots/", HotspotListView.as_view(), name="dashboard-hotspots"),
    path("clusters/<uuid:pk>/", ClusterDetailView.as_view(), name="dashboard-cluster-detail"),
]