/**
 * Public map (FR4): fetches /api/complaints/public-map/ and renders
 * every active complaint as a marker, color-coded by status. Attempts
 * to center on the browser's geolocation; falls back to a fixed
 * default center if permission is denied.
 */
const STATUS_COLORS = {
    received: "#6c757d",
    in_review: "#0d6efd",
    in_progress: "#fd7e14",
    resolved: "#198754",
};

let publicMap = null;

function initPublicMap(centerLat, centerLon) {
    publicMap = L.map("public-map").setView([centerLat, centerLon], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(publicMap);
}

async function loadPublicComplaints() {
    const response = await fetch("/api/complaints/public-map/", {
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    });
    if (!response.ok) {
        console.error("Failed to load public complaint map:", response.status);
        return;
    }
    const complaints = await response.json();
    complaints.forEach((c) => {
        const color = STATUS_COLORS[c.status] || "#6c757d";
        L.circleMarker([c.latitude, c.longitude], {
            radius: 7,
            color,
            fillColor: color,
            fillOpacity: 0.7,
        })
            .bindPopup(`<strong>${c.category || "Uncategorized"}</strong><br>Status: ${c.status}`)
            .addTo(publicMap);
    });
}

function startPublicMap() {
    const defaultCenter = [33.6844, 73.0479]; // Islamabad fallback
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                initPublicMap(pos.coords.latitude, pos.coords.longitude);
                loadPublicComplaints();
            },
            () => {
                initPublicMap(...defaultCenter);
                loadPublicComplaints();
            }
        );
    } else {
        initPublicMap(...defaultCenter);
        loadPublicComplaints();
    }
}

startPublicMap();