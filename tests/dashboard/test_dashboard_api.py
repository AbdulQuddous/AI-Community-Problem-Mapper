"""
Dashboard API tests: aggregation correctness, permission enforcement,
and hotspot filtering.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User
from apps.ai_engine.models import Cluster
from apps.complaints.models import Complaint


class DashboardStatsTests(APITestCase):
    def setUp(self):
        self.citizen = User.objects.create_user(
            username="dash_citizen", password="Pass!2024", role=Role.CITIZEN
        )
        self.authority = User.objects.create_user(
            username="dash_authority", password="Pass!2024", role=Role.AUTHORITY
        )
        Complaint.objects.create(
            user=self.citizen, description="Garbage complaint near market street.",
            latitude=33.6, longitude=73.0, category="garbage", priority_score=6.0,
        )
        Complaint.objects.create(
            user=self.citizen, description="Broken road near the school entrance.",
            latitude=33.7, longitude=73.1, category="roads", priority_score=8.0,
            status="resolved",
        )
        self.url = reverse("dashboard-stats")

    def test_citizen_forbidden(self):
        self.client.force_authenticate(user=self.citizen)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authority_gets_aggregated_stats(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["summary"]["total_complaints"], 2)
        self.assertEqual(response.data["summary"]["unresolved_count"], 1)

    def test_category_filter_applied(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.get(self.url, {"category": "garbage"})
        self.assertEqual(response.data["summary"]["total_complaints"], 1)


class HotspotListTests(APITestCase):
    def setUp(self):
        self.authority = User.objects.create_user(
            username="dash_authority2", password="Pass!2024", role=Role.AUTHORITY
        )
        Cluster.objects.create(
            category="garbage", centroid_latitude=33.6, centroid_longitude=73.0,
            complaint_count=7, is_hotspot=True,
        )
        Cluster.objects.create(
            category="roads", centroid_latitude=33.7, centroid_longitude=73.1,
            complaint_count=2, is_hotspot=False,
        )
        self.url = reverse("dashboard-hotspots")

    def test_only_hotspot_clusters_returned(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"] if "results" in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["category"], "garbage")


class ClusterDetailTests(APITestCase):
    def setUp(self):
        self.authority = User.objects.create_user(
            username="dash_authority3", password="Pass!2024", role=Role.AUTHORITY
        )
        self.cluster = Cluster.objects.create(
            category="water", centroid_latitude=33.6, centroid_longitude=73.0,
            complaint_count=5, is_hotspot=True, summary_text="Water shortage affecting multiple blocks.",
        )
        self.url = reverse("dashboard-cluster-detail", args=[self.cluster.id])

    def test_authority_can_view_summary(self):
        self.client.force_authenticate(user=self.authority)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("summary_text", response.data)