"""
Template shell view for the dashboard.

Note: does NOT use LoginRequiredMixin — our auth is JWT stored in
localStorage, not Django sessions, so LoginRequiredMixin's session
check always fails and redirects into a 405 loop against the JSON
login API. Auth/role gating for this page happens client-side (see
static/dashboard/js/dashboard.js) and is still enforced server-side
by every API call the page makes (IsAuthorityOrAdmin on the actual
data endpoints) — this view only serves the static HTML shell.
"""
from django.views.generic import TemplateView


class DashboardOverviewView(TemplateView):
    """GET /dashboard/ — HTML shell; data loads via authenticated fetch calls."""

    template_name = "dashboard/overview.html"