"""
Authentication tests: registration, login, role enforcement.

Covers FR1 (citizen registration/login) and the Phase 4 security
boundary that self-registration cannot grant authority/admin roles.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User


class RegistrationTests(APITestCase):
    """Tests for POST /api/auth/register/."""

    def setUp(self):
        self.url = reverse("register")
        self.valid_payload = {
            "username": "citizen_ali",
            "email": "ali@example.com",
            "phone_number": "03001234567",
            "password": "StrongPass!2024",
            "password_confirm": "StrongPass!2024",
        }

    def test_citizen_can_register(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="citizen_ali")
        self.assertEqual(user.role, Role.CITIZEN)

    def test_password_mismatch_rejected(self):
        payload = {**self.valid_payload, "password_confirm": "Different!2024"}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_role_field_in_request_is_ignored(self):
        """
        Security regression test: even if a client sends role=authority
        in the request body, the created user must still be a citizen.
        """
        payload = {**self.valid_payload, "role": Role.AUTHORITY}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="citizen_ali")
        self.assertEqual(user.role, Role.CITIZEN)

    def test_weak_password_rejected(self):
        payload = {**self.valid_payload, "password": "123", "password_confirm": "123"}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """Tests for POST /api/auth/login/ (SimpleJWT TokenObtainPairView)."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="citizen_sara",
            password="StrongPass!2024",
            role=Role.CITIZEN,
        )
        self.url = reverse("login")

    def test_valid_login_returns_tokens(self):
        response = self.client.post(
            self.url,
            {"username": "citizen_sara", "password": "StrongPass!2024"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials_rejected(self):
        response = self.client.post(
            self.url,
            {"username": "citizen_sara", "password": "WrongPassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeEndpointTests(APITestCase):
    """Tests for GET /api/auth/me/."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="authority_khan",
            password="StrongPass!2024",
            role=Role.AUTHORITY,
        )
        self.url = reverse("me")

    def test_unauthenticated_request_rejected(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_request_returns_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], Role.AUTHORITY)