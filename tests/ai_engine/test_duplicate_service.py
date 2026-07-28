"""
Tests for duplicate_service. Uses real cosine similarity math with
fixed embedding vectors — no mocking needed since this logic is pure
numpy, not an external call.
"""
from django.test import TestCase

from apps.accounts.models import Role, User
from apps.ai_engine.services.duplicate_service import find_duplicate
from apps.complaints.models import Complaint


class DuplicateServiceTests(TestCase):
    def setUp(self):
        self.citizen = User.objects.create_user(
            username="dup_tester", password="Pass!2024", role=Role.CITIZEN
        )

    def test_identical_embeddings_within_radius_flagged_duplicate(self):
        existing = Complaint.objects.create(
            user=self.citizen, description="Garbage piled up near the main gate area.",
            latitude=33.6844, longitude=73.0479, embedding=[1.0, 0.0, 0.0],
        )
        new_complaint = Complaint.objects.create(
            user=self.citizen, description="Trash accumulating near the main entrance area.",
            latitude=33.6845, longitude=73.0480, embedding=[1.0, 0.0, 0.0],
        )
        match = find_duplicate(new_complaint)
        self.assertEqual(match.id, existing.id)

    def test_dissimilar_embeddings_not_flagged(self):
        Complaint.objects.create(
            user=self.citizen, description="Garbage piled up near the main gate area.",
            latitude=33.6844, longitude=73.0479, embedding=[1.0, 0.0, 0.0],
        )
        new_complaint = Complaint.objects.create(
            user=self.citizen, description="Streetlight broken for two weeks on this road.",
            latitude=33.6845, longitude=73.0480, embedding=[0.0, 1.0, 0.0],
        )
        match = find_duplicate(new_complaint)
        self.assertIsNone(match)

    def test_similar_embedding_outside_geo_radius_not_flagged(self):
        Complaint.objects.create(
            user=self.citizen, description="Garbage piled up near the main gate area.",
            latitude=10.0, longitude=10.0, embedding=[1.0, 0.0, 0.0],
        )
        new_complaint = Complaint.objects.create(
            user=self.citizen, description="Trash accumulating near the main entrance area.",
            latitude=33.6845, longitude=73.0480, embedding=[1.0, 0.0, 0.0],
        )
        match = find_duplicate(new_complaint)
        self.assertIsNone(match)