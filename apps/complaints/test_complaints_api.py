"""
Complaint API tests: submission, scoping, filtering, status updates,
throttling, and signal-triggered enrichment.
"""
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
from apps.complaints.models import Complaint, ComplaintStatus


class ComplaintSubmissionTests(APITestCase):
    """Covers FR2, image validation, and the FR18 signal handoff."""

    def setUp(self):
        self.citizen = User.objects.create_user(
            username="citizen1", password="Pass!2024", role=Role.CITIZEN
        )
        self.client.force_authenticate(user=self.citizen)
        self.url = reverse("complaint-list")
        self.valid_payload = {
            "description": "There is a large pile of garbage on Main Street.",
            "latitude": 33.6844,
            "longitude": 73.0479,
        }

    def test_citizen_can_submit_complaint(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Complaint.objects.count(), 1)
        complaint = Complaint.objects.first()
        self.assertEqual(complaint.status, ComplaintStatus.RECEIVED)
        # AI fields must be null immediately after creation (FR19)
        self.assertIsNone(complaint.category)
        self.assertIsNone(complaint.priority_score)

    def test_short_description_rejected(self):
        payload = {**self.valid_payload, "description": "Too short"}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_latitude_rejected(self):
        payload = {**self.valid_payload, "latitude": 200.0}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_client_cannot_set_ai_fields(self):
        """AI fields sent by the client must be silently ignored, not applied."""
        payload = {**self.valid_payload, "category": "roads", "priority_score": 9.9}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        complaint = Complaint.objects.first()
        self.assertIsNone(complaint.category)
        self.assertIsNone(complaint.priority_score)

    @patch("apps.complaints.signals.threading.Thread")
    def test_enrichment_thread_started_on_create(self, mock_thread):
        """Verifies the post_save signal fires and starts a background thread."""
        self.client.post(self.url, self.valid_payload, format="json")
        mock_thread.assert_called_once()
        self.assertTrue(mock_thread.return_value.start.called)


class ComplaintScopingTests(APITestCase):
    """Covers FR3 (citizens see only their own) and authority full access."""

    def setUp(self):
        self.citizen_a = User.objects.create_user(
            username="citizenA", password="Pass!2024", role=Role.CITIZEN
        )
        self.citizen_b = User.objects.create_user(
            username="citizenB", password="Pass!2024", role=Role.CITIZEN
        )
        self.authority = User.objects.create_user(
            username="authority1", password="Pass!2024", role=Role.AUTHORITY
        )
        self.complaint_a = Complaint.objects.create(
            user=self.citizen_a, description="Garbage near park entrance area.",
            latitude=33.6, longitude=73.0,
        )
        self.complaint_b = Complaint.objects.create(
            user=self.citizen_b, description="Broken road near the market area.",
            latitude=33.7, longitude=73.1,
        )
        self.url = reverse("complaint-list")

    def test_citizen_sees_only_own_complaints(self):
        self.client.force_authenticate(user=self.citizen_a)
        response = self.client.get(self.url)
        ids = [c["id"] for c in response.data["results"]]
        self.assertIn(str(self.complaint_a.id), ids)
        self.assertNotIn(str(self.complaint_b.id), ids)

    def test_authority_sees_all_complaints(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 2)

    def test_citizen_cannot_retrieve_others_complaint(self):
        self.client.force_authenticate(user=self.citizen_a)
        response = self.client.get(reverse("complaint-detail", args=[self.complaint_b.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ComplaintStatusUpdateTests(APITestCase):
    """Covers FR16 and the transactional history write."""

    def setUp(self):
        self.citizen = User.objects.create_user(
            username="citizen2", password="Pass!2024", role=Role.CITIZEN
        )
        self.authority = User.objects.create_user(
            username="authority2", password="Pass!2024", role=Role.AUTHORITY
        )
        self.complaint = Complaint.objects.create(
            user=self.citizen, description="Sewer overflow near residential block.",
            latitude=33.6, longitude=73.0,
        )
        self.url = reverse("complaint-update-status", args=[self.complaint.id])

    def test_authority_can_update_status(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.patch(self.url, {"status": "in_review"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, "in_review")
        self.assertEqual(self.complaint.status_history.count(), 1)

    def test_citizen_cannot_update_status(self):
        self.client.force_authenticate(user=self.citizen)
        response = self.client.patch(self.url, {"status": "in_review"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_status_rejected(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.patch(self.url, {"status": "not_a_real_status"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)