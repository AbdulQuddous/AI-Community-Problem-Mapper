"""
Local complaint classifier — replaces the Gemini classification call
(FR7) with a small scikit-learn model trained on top of the Sentence
Transformer embeddings we already generate for every complaint.

Design contract (matches classification_service.classify_complaint's
contract exactly, so enrichment_service.py can swap between them):
  - Takes an already-computed embedding (list[float]), not raw text —
    avoids re-encoding, since embedding_service already ran in Step 2.
  - Returns a valid category string, or None if the model is
    unavailable or its confidence is below
    settings.LOCAL_CLASSIFIER_CONFIDENCE_THRESHOLD (mirrors FR19's
    "leave the field null rather than guess" contract).
  - Never raises — any loading/prediction error is caught and logged,
    returning None so the caller can fall back to Gemini.
"""
import logging

import joblib
from django.conf import settings

logger = logging.getLogger("ai_engine")

_model_bundle = None
_load_failed = False


def _load_model():
    """
    Lazily load the trained classifier bundle once per process.

    The bundle is a dict with keys "classifier" (a fitted sklearn
    Pipeline/estimator) and "label_encoder" (maps model output
    indices back to category strings) — saved together by
    scripts/train_classifier.py so loading is a single joblib.load
    call with no separate label-mapping file to keep in sync.
    """
    global _model_bundle, _load_failed
    if _model_bundle is not None or _load_failed:
        return

    try:
        _model_bundle = joblib.load(settings.LOCAL_CLASSIFIER_MODEL_PATH)
        logger.info("Local classifier model loaded from %s", settings.LOCAL_CLASSIFIER_MODEL_PATH)
    except FileNotFoundError:
        logger.warning(
            "Local classifier model not found at %s — run scripts/train_classifier.py. "
            "Falling back to Gemini classification.",
            settings.LOCAL_CLASSIFIER_MODEL_PATH,
        )
        _load_failed = True
    except Exception as exc:  # noqa: BLE001 — any load failure must not crash enrichment
        logger.error("Failed to load local classifier model: %s", exc)
        _load_failed = True


def classify_complaint_local(embedding: list) -> str | None:
    """
    Classify a complaint using the locally trained model, given its
    already-computed embedding.

    Returns None if the model isn't available or confidence is below
    threshold — callers should treat this exactly like a Gemini
    classification failure (leave Complaint.category null, or fall
    back to Gemini classification_service).
    """
    _load_model()
    if _model_bundle is None:
        return None

    try:
        classifier = _model_bundle["classifier"]
        label_encoder = _model_bundle["label_encoder"]

        probabilities = classifier.predict_proba([embedding])[0]
        best_index = probabilities.argmax()
        best_confidence = probabilities[best_index]

        if best_confidence < settings.LOCAL_CLASSIFIER_CONFIDENCE_THRESHOLD:
            logger.info(
                "Local classifier confidence too low (%.2f < %.2f); returning None.",
                best_confidence, settings.LOCAL_CLASSIFIER_CONFIDENCE_THRESHOLD,
            )
            return None

        category = label_encoder.inverse_transform([best_index])[0]
        logger.info("Local classifier predicted '%s' (confidence %.2f)", category, best_confidence)
        return category
    except Exception as exc:  # noqa: BLE001 — prediction failure must not crash enrichment
        logger.error("Local classifier prediction failed: %s", exc)
        return None