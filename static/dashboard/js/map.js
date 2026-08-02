/**
 * Loads /api/dashboard/hotspots/ and renders them as Leaflet markers
 * (FR14). Clicking a marker fetches the cluster detail (including the
 * Gemini summary, US4) on demand rather than loading it upfront for
 * every hotspot, keeping the initial page load light.
 */
let map = null;
let markersLayer = null;

function initMap() {
    map = L.map("hotspot-map").setView([33.6844, 73.0479], 12); // default: Islamabad
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);
    markersLayer = L.layerGroup().addTo(map);
}

async function loadHotspots() {
    const response = await fetch("/api/dashboard/hotspots/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    });
    if (!response.ok) {
        console.error("Failed to load hotspots:", response.status);
        return;
    }
    const data = await response.json();
    const hotspots = data.results || data;

    markersLayer.clearLayers();
    hotspots.forEach((cluster) => {
        const marker = L.circleMarker(
            [cluster.centroid_latitude, cluster.centroid_longitude],
            { radius: 8 + Math.min(cluster.complaint_count, 20), color: "#dc3545" }
        );
        marker.bindPopup(
            `<strong>${cluster.category}</strong><br>` +
            `${cluster.complaint_count} complaints<br>` +
            `Priority: ${cluster.priority_score ?? "N/A"}<br>` +
            `<button onclick="loadClusterDetail('${cluster.id}')" class="btn btn-sm btn-outline-primary mt-1">View Summary</button>`
        );
        marker.addTo(markersLayer);
    });
}

async function loadClusterDetail(clusterId) {
    const response = await fetch(`/api/dashboard/clusters/${clusterId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    });
    if (!response.ok) return;
    const cluster = await response.json();
    alert(cluster.summary_text || "Summary not yet generated for this cluster.");
}

initMap();
loadHotspots();