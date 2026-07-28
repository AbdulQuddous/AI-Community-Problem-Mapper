"""
Tests for clustering_service. Runs real DBSCAN (cheap, local, no
mocking needed) over a small synthetic set of complaints.
"""
from django.test import TestCase

from apps.accounts.models import Role, User
from apps.ai_engine.models import Cluster
from apps.ai_engine.services.clustering_service import assign_cluster
from apps.complaints.models import Complaint


class ClusteringServiceTests(TestCase):
    def setUp(self):
        self.citizen = User.objects.create_user(
            username="cluster_tester", password="Pass!2024", role=Role.CITIZEN
        )

    def _make_complaint(self, lat, lon):
        return Complaint.objects.create(
            user=self.citizen, description="Garbage accumulating near this location today.",
            latitude=lat, longitude=lon, category="garbage",
        )

    def test_dense_group_forms_a_cluster(self):
        # Three complaints within ~100m of each other -> should cluster
        c1 = self._make_complaint(33.6844, 73.0479)
        self._make_complaint(33.6845, 73.0480)
        self._make_complaint(33.6846, 73.0481)

        cluster = assign_cluster(c1)
        self.assertIsNotNone(cluster)
        self.assertGreaterEqual(cluster.complaint_count, 3)

    def test_isolated_complaint_below_min_samples_not_clustered(self):
        c1 = self._make_complaint(33.6844, 73.0479)
        cluster = assign_cluster(c1)
        self.assertIsNone(cluster)  # only 1 complaint, below DBSCAN_MIN_SAMPLES

    def test_far_apart_complaints_do_not_share_a_cluster(self):
        c1 = self._make_complaint(33.6844, 73.0479)
        self._make_complaint(33.6845, 73.0480)
        self._make_complaint(33.6846, 73.0481)
        far_complaint = self._make_complaint(10.0, 10.0)  # far away

        cluster = assign_cluster(far_complaint)
        self.assertIsNone(cluster)