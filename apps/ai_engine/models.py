"""
Cluster model — the persisted output of the DBSCAN clustering service
(Phase 6) and the Gemini summarization service.

A Cluster is a first-class entity because its state (summary,
hotspot flag, priority) outlives any single clustering run and must
be readable by the dashboard without recomputation on every request.
"""
from django.db import models

from apps.common.models import BaseModel


class Cluster(BaseModel):
    """
    Represents a group of semantically + geographically related
    complaints, as produced by the DBSCAN clustering service.

    Fields:
        category: Dominant complaint category within this cluster.
        centroid_latitude / centroid_longitude: Geographic center,
            used to place the cluster marker on the map (FR14).
        complaint_count: Denormalized count, refreshed each time the
            clustering service runs, to avoid a COUNT() query on every
            dashboard load.
        priority_score: Gemini-estimated priority for this cluster
            (FR10), null until the Gemini call succeeds (FR19).
        summary_text: Gemini-generated summary (FR12), null until
            generated.
        is_hotspot: Set True when complaint_count/density crosses the
            configurable DBSCAN threshold (FR11).
    """

    category = models.CharField(max_length=50)
    centroid_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    centroid_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    complaint_count = models.PositiveIntegerField(default=0)
    priority_score = models.FloatField(null=True, blank=True)
    summary_text = models.TextField(null=True, blank=True)
    is_hotspot = models.BooleanField(default=False)

    class Meta:
        db_table = "ai_engine_cluster"
        indexes = [
            models.Index(fields=["is_hotspot"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self) -> str:
        return f"Cluster[{self.category}] ({self.complaint_count} complaints)"