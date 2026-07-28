"""
Embedding generation service (FR6) using Sentence Transformers.

The model is loaded once as a lazy module-level singleton — see
Phase 6 Architecture Discussion (2.2) for why. Callers should never
instantiate SentenceTransformer directly; always go through
generate_embedding().
"""
import logging

from sentence_transformers import SentenceTransformer

from django.conf import settings

logger = logging.getLogger("ai_engine")

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(
            "Loading Sentence Transformer model: %s", settings.SENTENCE_TRANSFORMER_MODEL
        )
        _model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
    return _model


def generate_embedding(text: str) -> list[float]:
    """
    Generate a semantic embedding for the given text.

    Returns a plain Python list of floats (JSON-serializable), since
    Complaint.embedding is a JSONField (Phase 2 tradeoff: no pgvector
    in MVP).
    """
    model = _get_model()
    vector = model.encode(text, convert_to_numpy=True)
    return vector.tolist()