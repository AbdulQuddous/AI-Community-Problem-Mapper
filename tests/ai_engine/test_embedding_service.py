"""
Tests for embedding_service. Mocks SentenceTransformer entirely —
tests must not load the real model (slow, and CI may lack the weights
cached), only verify the service's contract: text in, list[float] out.
"""
from unittest.mock import MagicMock, patch

from django.test import TestCase


class EmbeddingServiceTests(TestCase):
    @patch("apps.ai_engine.services.embedding_service.SentenceTransformer")
    def test_generate_embedding_returns_list_of_floats(self, mock_st_class):
        import numpy as np

        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])
        mock_st_class.return_value = mock_model

        import apps.ai_engine.services.embedding_service as svc
        svc._model = None  # reset singleton for test isolation

        result = svc.generate_embedding("There is garbage on the street")
        self.assertEqual(result, [0.1, 0.2, 0.3])
        self.assertIsInstance(result, list)

    @patch("apps.ai_engine.services.embedding_service.SentenceTransformer")
    def test_model_loaded_only_once(self, mock_st_class):
        import apps.ai_engine.services.embedding_service as svc
        svc._model = None

        mock_model = MagicMock()
        mock_model.encode.return_value = __import__("numpy").array([0.1])
        mock_st_class.return_value = mock_model

        svc.generate_embedding("text one")
        svc.generate_embedding("text two")
        mock_st_class.assert_called_once()