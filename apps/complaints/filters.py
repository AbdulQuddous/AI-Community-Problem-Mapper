"""
django-filter FilterSet for Complaint list endpoint (FR15).

Kept separate from views.py so filtering rules are declarative and
independently testable, per the master prompt's clean-architecture
requirement.
"""
import django_filters

from apps.complaints.models import Complaint


class ComplaintFilter(django_filters.FilterSet):
    """
    Supports filtering by category, status, and a created_at date
    range — the exact filter set specified in FR15.
    """

    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Complaint
        fields = ["category", "status", "date_from", "date_to"]