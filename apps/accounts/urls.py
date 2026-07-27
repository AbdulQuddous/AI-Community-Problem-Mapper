"""
URL routing for authentication.

TokenObtainPairView/TokenRefreshView come directly from SimpleJWT —
no custom login view is written, since the default behavior already
satisfies FR (JWT login) exactly.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import MeView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),
    path("me/", MeView.as_view(), name="me"),
]