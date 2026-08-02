"""
Template shell view for the dashboard. Renders a static HTML page
that loads data client-side via the API views in api_views.py — see
Phase 7 Architecture Discussion (2.2) for why logic isn't duplicated
here.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from apps.accounts.models import Role


class DashboardOverviewView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    GET /dashboard/ (template route, not under /api/)

    Restricted to authority/admin at the view level, mirroring the
    API-level IsAuthorityOrAdmin permission — a citizen hitting this
    URL directly should be blocked here too, not only when their
    browser's fetch calls to the API start failing.
    """

    template_name = "dashboard/overview.html"
    login_url = "/api/auth/login/"  # citizens/authorities log in via API + store JWT client-side

    def test_func(self) -> bool:
        return self.request.user.role in (Role.AUTHORITY, Role.ADMIN)