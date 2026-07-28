"""
Integration-style tests for the enrichment orchestrator. Mocks every
external/expensive dependency (embedding model, Gemini calls) so the
test verifies orchestration logic and the FR19 fallback contract,
not the underlying AI services (already covered by their own tests).
"""
from unittest.mock import patch

from django.test import TestCase

from apps.accounts.models import Role, User
from apps.ai_engine.services.enrichment_service import enrich_complaint
from apps.complaints.models import Complaint
from core.exceptions import AIServiceUnavailableError


class EnrichmentServiceTests(TestCase):
    def setUp(self):
        self.citizen = User.objects.create_user(
            username="enrich_tester", password="Pass!2024", role=Role.CITIZEN
        )
        self.complaint = Complaint.objects.create(
            user=self.citizen, description="Garbage has been piling up near the market.",
            latitude=33.6844, longitude=73.0479,
        )

    @patch("apps.ai_engine.services.enrichment_service.summarization_service.summarize_cluster")
    @patch("apps.ai_engine.services.enrichment_service.priority_service.estimate_priority")
    @patch("apps.ai_engine.services.enrichment_service.clustering_service.assign_cluster")
    @patch("apps.ai_engine.services.enrichment_service.classification_service.classify_complaint")
    @patch("apps.ai_engine.services.enrichment_service.duplicate_service.find_duplicate")
    @patch("apps.ai_engine.services.enrichment_service.embedding_service.generate_embedding")
    def test_full_pipeline_success(
        self, mock_embed, mock_dup, mock_classify, mock_cluster, mock_priority, mock_summary
    ):
        mock_embed.return_value = [0.1, 0.2]
        mock_dup.return_value = None
        mock_classify.return_value = "garbage"
        mock_cluster.return_value = None  # not enough complaints to cluster
        mock_priority.return_value = 7.0

        enrich_complaint(str(self.complaint.id))

        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.category, "garbage")
        self.assertEqual(self.complaint.priority_score, 7.0)
        self.assertIsNotNone(self.complaint.embedding)

    @patch("apps.ai_engine.services.enrichment_service.duplicate_service.find_duplicate")
    @patch("apps.ai_engine.services.enrichment_service.embedding_service.generate_embedding")
    def test_duplicate_short_circuits_pipeline(self, mock_embed, mock_dup):
        original = Complaint.objects.create(
            user=self.citizen, description="Original garbage complaint near market entrance.",
            latitude=33.6844, longitude=73.0479,
        )
        mock_embed.return_value = [0.1, 0.2]
        mock_dup.return_value = original

        enrich_complaint(str(self.complaint.id))

        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.duplicate_of_id, original.id)
        self.assertIsNone(self.complaint.category)  # classification never ran

    @patch("apps.ai_engine.services.enrichment_service.classification_service.classify_complaint")
    @patch("apps.ai_engine.services.enrichment_service.duplicate_service.find_duplicate")
    @patch("apps.ai_engine.services.enrichment_service.embedding_service.generate_embedding")
    def test_gemini_classification_failure_leaves_category_null(
        self, mock_embed, mock_dup, mock_classify
    ):
        """FR19: Gemini failure must not crash enrichment or corrupt the row."""
        mock_embed.return_value = [0.1, 0.2]
        mock_dup.return_value = None
        mock_classify.return_value = None  # simulates classify_complaint's own fallback

        enrich_complaint(str(self.complaint.id))

        self.complaint.refresh_from_db()
        self.assertIsNone(self.complaint.category)
        self.assertIsNone(self.complaint.priority_score)  # never reached, no crash

    def test_nonexistent_complaint_does_not_raise(self):
        """Must never raise, since this runs on an unattended daemon thread."""
        try:
            enrich_complaint("00000000-0000-0000-0000-000000000000")
        except Exception as exc:  # noqa: BLE001
            self.fail(f"enrich_complaint raised unexpectedly: {exc}")