"""
Tests for the public map endpoint: field-level privacy boundary and
status filtering.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
from apps.complaints.models import Complaint


class PublicMapTests(APITestCase):
    def setUp(self):
        self.citizen_a = User.objects.create_user(
            username="pubmap_a", password="Pass!2024", role=Role.CITIZEN
        )
        self.citizen_b = User.objects.create_user(
            username="pubmap_b", password="Pass!2024", role=Role.CITIZEN
        )
        self.active_complaint = Complaint.objects.create(
            user=self.citizen_a, description="Garbage piled up near the main road.",
            latitude=33.6844, longitude=73.0479, category="garbage", status="received",
        )
        self.resolved_complaint = Complaint.objects.create(
            user=self.citizen_a, description="Previously broken streetlight, now fixed.",
            latitude=33.6845, longitude=73.0480, category="streetlights", status="resolved",
        )
        self.url = reverse("complaint-public-map")

    def test_unauthenticated_request_rejected(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_any_authenticated_citizen_can_view(self):
        """A different citizen (not the reporter) can still see the pin."""
        self.client.force_authenticate(user=self.citizen_b)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [c["id"] for c in response.data]
        self.assertIn(str(self.active_complaint.id), ids)

    def test_resolved_complaints_excluded(self):
        self.client.force_authenticate(user=self.citizen_b)
        response = self.client.get(self.url)
        ids = [c["id"] for c in response.data]
        self.assertNotIn(str(self.resolved_complaint.id), ids)

    def test_response_excludes_reporter_identity(self):
        """Privacy boundary: user field must never appear in this payload."""
        self.client.force_authenticate(user=self.citizen_b)
        response = self.client.get(self.url)
        entry = next(c for c in response.data if c["id"] == str(self.active_complaint.id))
        self.assertNotIn("user", entry)
        self.assertNotIn("description", entry)
        self.assertNotIn("image", entry)