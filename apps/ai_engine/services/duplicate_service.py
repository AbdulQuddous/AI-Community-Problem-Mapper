"""
Duplicate detection service (FR8).

Geo-bounded prefilter, then cosine similarity — see Phase 6
Architecture Discussion (2.3) for why this two-stage approach rather
than a global embedding scan.
"""
import logging
from datetime import timedelta

import numpy as np
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger("ai_engine")


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr, b_arr = np.array(a), np.array(b)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


def _bounding_box(lat: float, lon: float, radius_km: float) -> tuple[float, float, float, float]:
    """
    Rough lat/lon bounding box for a given radius — a cheap prefilter,
    not exact great-circle math. 1 degree latitude ~= 111km; longitude
    degrees shrink with latitude, approximated here as a fixed 111km
    too, which over-includes slightly near the poles but is more than
    accurate enough for a single-city deployment.
    """
    delta = radius_km / 111.0
    return lat - delta, lat + delta, lon - delta, lon + delta


def find_duplicate(complaint) -> object | None:
    """
    Search for a near-duplicate of `complaint` among recent, unresolved
    complaints within DUPLICATE_GEO_RADIUS_KM.

    Args:
        complaint: a Complaint instance with .embedding already populated.

    Returns:
        The matching Complaint instance if a duplicate is found above
        DUPLICATE_SIMILARITY_THRESHOLD, else None.
    """
    from apps.complaints.models import Complaint  # local import: avoid
    # circular import (complaints -> ai_engine -> complaints)

    if not complaint.embedding:
        return None

    lat_min, lat_max, lon_min, lon_max = _bounding_box(
        float(complaint.latitude), float(complaint.longitude), settings.DUPLICATE_GEO_RADIUS_KM
    )
    window_start = timezone.now() - timedelta(days=settings.CLUSTERING_WINDOW_DAYS)

    candidates = Complaint.objects.filter(
        is_deleted=False,
        embedding__isnull=False,
        latitude__gte=lat_min, latitude__lte=lat_max,
        longitude__gte=lon_min, longitude__lte=lon_max,
        created_at__gte=window_start,
    ).exclude(id=complaint.id).exclude(status="resolved")

    best_match, best_score = None, 0.0
    for candidate in candidates:
        score = _cosine_similarity(complaint.embedding, candidate.embedding)
        if score > best_score:
            best_match, best_score = candidate, score

    if best_match and best_score >= settings.DUPLICATE_SIMILARITY_THRESHOLD:
        logger.info(
            "Duplicate found: complaint=%s matches=%s score=%.3f",
            complaint.id, best_match.id, best_score,
        )
        return best_match
    return None