"""
Tests for local_classifier_service. Mocks joblib.load entirely so
tests never depend on an actual trained model file existing.
"""
from unittest.mock import MagicMock, patch

from django.test import TestCase


class LocalClassifierServiceTests(TestCase):
    def setUp(self):
        import apps.ai_engine.services.local_classifier_service as svc
        svc._model_bundle = None
        svc._load_failed = False

    @patch("apps.ai_engine.services.local_classifier_service.joblib.load")
    def test_confident_prediction_returns_category(self, mock_load):
        import numpy as np

        mock_classifier = MagicMock()
        mock_classifier.predict_proba.return_value = np.array([[0.05, 0.9, 0.05]])
        mock_encoder = MagicMock()
        mock_encoder.inverse_transform.return_value = ["garbage"]
        mock_load.return_value = {"classifier": mock_classifier, "label_encoder": mock_encoder}

        from apps.ai_engine.services.local_classifier_service import classify_complaint_local
        result = classify_complaint_local([0.1] * 384)
        self.assertEqual(result, "garbage")

    @patch("apps.ai_engine.services.local_classifier_service.joblib.load")
    def test_low_confidence_returns_none(self, mock_load):
        import numpy as np

        mock_classifier = MagicMock()
        mock_classifier.predict_proba.return_value = np.array([[0.4, 0.35, 0.25]])
        mock_load.return_value = {"classifier": mock_classifier, "label_encoder": MagicMock()}

        from apps.ai_engine.services.local_classifier_service import classify_complaint_local
        result = classify_complaint_local([0.1] * 384)
        self.assertIsNone(result)

    @patch("apps.ai_engine.services.local_classifier_service.joblib.load")
    def test_missing_model_file_returns_none(self, mock_load):
        mock_load.side_effect = FileNotFoundError()

        from apps.ai_engine.services.local_classifier_service import classify_complaint_local
        result = classify_complaint_local([0.1] * 384)
        self.assertIsNone(result)

    @patch("apps.ai_engine.services.local_classifier_service.joblib.load")
    def test_model_loaded_only_once(self, mock_load):
        import numpy as np

        mock_classifier = MagicMock()
        mock_classifier.predict_proba.return_value = np.array([[0.1, 0.8, 0.1]])
        mock_encoder = MagicMock()
        mock_encoder.inverse_transform.return_value = ["roads"]
        mock_load.return_value = {"classifier": mock_classifier, "label_encoder": mock_encoder}

        from apps.ai_engine.services.local_classifier_service import classify_complaint_local
        classify_complaint_local([0.1] * 384)
        classify_complaint_local([0.2] * 384)
        mock_load.assert_called_once()