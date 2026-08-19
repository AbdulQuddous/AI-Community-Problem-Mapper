"""
Duplicate detection service (FR8).

Now that the system is English-only, all complaint embeddings are
produced from same-script, same-language text — the severe
similarity-score unreliability we previously saw with Roman Urdu
(scores as low as 0.15-0.3 for genuine duplicates) no longer applies.
The exact-location + same-category short-circuit tier is retained as
a light safety net for edge cases (very short descriptions, unusual
phrasing) rather than as a primary mechanism.
"""
import logging
import math
from datetime import timedelta

import numpy as np
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger("ai_engine")


def _cosine_similarity(a: list, b: list) -> float:
    a_arr, b_arr = np.array(a), np.array(b)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


def _bounding_box(lat: float, lon: float, radius_km: float) -> tuple:
    delta = radius_km / 111.0
    return lat - delta, lat + delta, lon - delta, lon + delta


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(a))


def _resolve_root(complaint) -> object:
    """
    Follows duplicate_of up to the original, non-duplicate complaint.
    Guards against a pathological multi-hop chain (shouldn't occur
    given this function is always used, but defensive nonetheless)
    with a max hop limit.
    """
    root = complaint
    hops = 0
    # Prevent infinite loops with a reasonable max depth
    while root.duplicate_of_id is not None and hops < 5:
        root = root.duplicate_of
        hops += 1
    
    if hops >= 5:
        logger.warning(
            "Duplicate chain exceeded 5 hops for complaint %s, stopping at %s",
            complaint.id, root.id
        )
    
    return root


def find_duplicate(complaint) -> object | None:
    """
    Search for a near-duplicate of `complaint` among recent, unresolved
    complaints within DUPLICATE_GEO_RADIUS_KM.

    Always returns the ROOT complaint of a duplicate chain, never an
    intermediate duplicate — this keeps duplicate_of chains exactly
    one level deep (main complaint <- duplicates), matching the
    assumption baked into the Manage Complaints page (see
    manage_serializers.py). Without this resolution, a third report
    of the same issue could end up pointing to the second report
    (itself a duplicate) instead of the original, orphaning it from
    the manage page's one-level nesting.

    Tiers:
      1. Exact-location + same-category short-circuit: safety net for
         edge cases where embedding similarity might understate an
         obvious duplicate (e.g. very short/terse descriptions).
      2. Standard embedding similarity threshold
         (DUPLICATE_SIMILARITY_THRESHOLD) for everything else.
    """
    from apps.complaints.models import Complaint

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
        same_category = bool(
            complaint.category and candidate.category and complaint.category == candidate.category
        )
        distance_km = _haversine_km(
            float(complaint.latitude), float(complaint.longitude),
            float(candidate.latitude), float(candidate.longitude),
        )
        is_exact_location = distance_km <= settings.DUPLICATE_EXACT_LOCATION_RADIUS_KM

        # Tier 1: short-circuit, no embedding check needed at all.
        if is_exact_location and same_category:
            # CRITICAL: Resolve to the root original
            root = _resolve_root(candidate)
            logger.info(
                "Duplicate found (location+category short-circuit): complaint=%s matches=%s "
                "(resolved to root=%s) distance_km=%.4f",
                complaint.id, candidate.id, root.id, distance_km,
            )
            return root

        score = _cosine_similarity(complaint.embedding, candidate.embedding)
        if score >= settings.DUPLICATE_SIMILARITY_THRESHOLD and score > best_score:
            best_match, best_score = candidate, score

    if best_match:
        # CRITICAL: Resolve to the root original
        root = _resolve_root(best_match)
        logger.info(
            "Duplicate found: complaint=%s matches=%s (resolved to root=%s) score=%.3f",
            complaint.id, best_match.id, root.id, best_score,
        )
        return root
    return None