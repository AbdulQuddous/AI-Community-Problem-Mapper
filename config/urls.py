"""
Root URL configuration.

Per-app URL modules (accounts, complaints, dashboard) are added in
their respective phases (4, 5, 7) — this file only establishes the
top-level routing skeleton now.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.dashboard.views import DashboardOverviewView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/complaints/", include("apps.complaints.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),  # now resolves — Phase 7
    path("dashboard/", DashboardOverviewView.as_view(), name="dashboard-overview"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)