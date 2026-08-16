"""
Authentication views: registration and JWT login.

Login itself is handled by SimpleJWT's built-in TokenObtainPairView
(wired directly in urls.py) — no custom view needed there, since it
already does exactly what FR requires (issue access + refresh tokens
against username/password). RegisterView is the only custom view
this app needs at this phase.
"""
import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.accounts.serializers import RegisterSerializer, UserSerializer

logger = logging.getLogger("django")


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/

    Public endpoint for citizen self-registration (FR1). Role is
    always CITIZEN regardless of request body — see serializer.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info("New citizen registered: user_id=%s", user.id)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class MeView(generics.RetrieveAPIView):
    """
    GET /api/auth/me/

    Returns the authenticated user's own profile. Used by the
    frontend to determine role and render the correct dashboard vs.
    citizen view (Phase 7/8).
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

from django.views.generic import TemplateView


class LoginPageView(TemplateView):
    """GET /accounts/login/ — HTML login form (posts to /api/auth/login/ via JS)."""

    template_name = "accounts/login.html"


class RegisterPageView(TemplateView):
    """GET /accounts/register/ — HTML registration form."""

    template_name = "accounts/register.html"