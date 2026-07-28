"""
Tests for classification_service. Mocks call_gemini entirely — tests
never make real API calls.
"""
from unittest.mock import patch

from django.test import TestCase

from apps.ai_engine.services.classification_service import classify_complaint
from core.exceptions import AIServiceUnavailableError


class ClassificationServiceTests(TestCase):
    @patch("apps.ai_engine.services.classification_service.call_gemini")
    def test_valid_category_returned(self, mock_call):
        mock_call.return_value = "garbage"
        result = classify_complaint("There is garbage on the street")
        self.assertEqual(result, "garbage")

    @patch("apps.ai_engine.services.classification_service.call_gemini")
    def test_invalid_category_returns_none(self, mock_call):
        mock_call.return_value = "not_a_real_category"
        result = classify_complaint("Something ambiguous")
        self.assertIsNone(result)

    @patch("apps.ai_engine.services.classification_service.call_gemini")
    def test_gemini_unavailable_returns_none(self, mock_call):
        mock_call.side_effect = AIServiceUnavailableError("timeout")
        result = classify_complaint("There is garbage on the street")
        self.assertIsNone(result)