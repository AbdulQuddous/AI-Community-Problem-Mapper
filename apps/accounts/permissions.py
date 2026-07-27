"""
Custom role-based DRF permission classes.

One class per role, deliberately, for readability in view definitions
— see Phase 4 Architecture Discussion (section 2.4).
"""
from rest_framework.permissions import BasePermission

from apps.accounts.models import Role


class IsCitizen(BasePermission):
    """Grants access only to authenticated users with the citizen role."""

    message = "This action is restricted to citizen accounts."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.CITIZEN
        )


class IsAuthority(BasePermission):
    """Grants access only to municipal authority accounts."""

    message = "This action is restricted to municipal authority accounts."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.AUTHORITY
        )


class IsAdmin(BasePermission):
    """Grants access only to city administrator accounts."""

    message = "This action is restricted to administrator accounts."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.ADMIN
        )


class IsAuthorityOrAdmin(BasePermission):
    """
    Grants access to either authority or admin accounts.

    Used on dashboard/complaint-management endpoints (Phase 5, 7)
    where both roles have equivalent read/update access, per Phase 1's
    Primary Users definition.
    """

    message = "This action requires municipal authority or administrator access."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (Role.AUTHORITY, Role.ADMIN)
        )


class IsOwnerOrAuthorityOrAdmin(BasePermission):
    """
    Object-level permission: citizens may only access their own
    objects (e.g., their own complaints); authority/admin may access
    any object. Used in Phase 5 on Complaint detail/update views.
    """

    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.role in (Role.AUTHORITY, Role.ADMIN):
            return True
        return getattr(obj, "user_id", None) == request.user.id