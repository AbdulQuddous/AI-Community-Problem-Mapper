"""
Clustering and hotspot detection service (FR9, FR9A, FR11) — DBSCAN.

Runs on haversine geographic distance, scoped to complaints of the
same category, per the tradeoff documented in Phase 6 Architecture
Discussion (2.4). Bounded to CLUSTERING_WINDOW_DAYS (FR9A) to keep
the operation cheap as complaint volume grows.
"""
import logging
import math
from datetime import timedelta

import numpy as np
from django.conf import settings
from django.utils import timezone
from sklearn.cluster import DBSCAN

logger = logging.getLogger("ai_engine")

EARTH_RADIUS_KM = 6371.0


def _haversine_matrix(coords_rad: np.ndarray) -> np.ndarray:
    """Pairwise haversine distance matrix (km) for an array of [lat, lon] in radians."""
    n = len(coords_rad)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            lat1, lon1 = coords_rad[i]
            lat2, lon2 = coords_rad[j]
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            d = 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))
            dist[i, j] = dist[j, i] = d
    return dist


def assign_cluster(complaint) -> object | None:
    """
    Run DBSCAN over recent, active, same-category complaints (including
    `complaint` itself) and assign/create the appropriate Cluster row.

    Returns:
        The Cluster instance the complaint was assigned to, or None if
        the complaint didn't fall into any dense group (DBSCAN noise
        point) or has no category yet (classification must run first).
    """
    from apps.ai_engine.models import Cluster
    from apps.complaints.models import Complaint

    if not complaint.category:
        return None

    window_start = timezone.now() - timedelta(days=settings.CLUSTERING_WINDOW_DAYS)
    active_complaints = list(
        Complaint.objects.filter(
            is_deleted=False,
            category=complaint.category,
            created_at__gte=window_start,
        ).exclude(status="resolved")
    )
    if complaint not in active_complaints:
        active_complaints.append(complaint)

    if len(active_complaints) < settings.DBSCAN_MIN_SAMPLES:
        return None

    coords_rad = np.radians(
        [[float(c.latitude), float(c.longitude)] for c in active_complaints]
    )
    dist_matrix = _haversine_matrix(coords_rad)

    db = DBSCAN(
        eps=settings.DBSCAN_EPS_KM,
        min_samples=settings.DBSCAN_MIN_SAMPLES,
        metric="precomputed",
    )
    labels = db.fit_predict(dist_matrix)

    complaint_index = active_complaints.index(complaint)
    label = labels[complaint_index]
    if label == -1:
        logger.info("Complaint %s is a DBSCAN noise point; no cluster assigned.", complaint.id)
        return None

    group = [c for c, lbl in zip(active_complaints, labels) if lbl == label]
    centroid_lat = sum(float(c.latitude) for c in group) / len(group)
    centroid_lon = sum(float(c.longitude) for c in group) / len(group)

    cluster = _find_or_create_cluster(
        category=complaint.category,
        centroid_lat=centroid_lat,
        centroid_lon=centroid_lon,
        complaint_count=len(group),
    )

    Complaint.objects.filter(id__in=[c.id for c in group]).update(cluster=cluster)
    return cluster


def _find_or_create_cluster(category: str, centroid_lat: float, centroid_lon: float, complaint_count: int):
    """
    Reuse an existing Cluster if one already represents this
    category+area (by centroid proximity), else create a new one.
    See Phase 6 Architecture Discussion (2.5).
    """
    from apps.ai_engine.models import Cluster

    candidates = Cluster.objects.filter(category=category, is_deleted=False)
    for existing in candidates:
        d = _haversine_point(
            centroid_lat, centroid_lon,
            float(existing.centroid_latitude), float(existing.centroid_longitude),
        )
        if d <= settings.CLUSTER_MATCH_RADIUS_KM:
            existing.centroid_latitude = centroid_lat
            existing.centroid_longitude = centroid_lon
            existing.complaint_count = complaint_count
            existing.is_hotspot = complaint_count >= settings.HOTSPOT_MIN_COMPLAINTS
            existing.save(update_fields=[
                "centroid_latitude", "centroid_longitude", "complaint_count", "is_hotspot", "updated_at"
            ])
            return existing

    new_cluster = Cluster.objects.create(
        category=category,
        centroid_latitude=centroid_lat,
        centroid_longitude=centroid_lon,
        complaint_count=complaint_count,
        is_hotspot=complaint_count >= settings.HOTSPOT_MIN_COMPLAINTS,
    )
    logger.info("New cluster created: id=%s category=%s size=%d", new_cluster.id, category, complaint_count)
    return new_cluster


def _haversine_point(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))