/**
 * Location picker (supports FR2): a single draggable/clickable Leaflet
 * marker bound to the #latitude/#longitude hidden inputs, plus the
 * submission handler that POSTs to /api/complaints/. Reuses the same
 * Leaflet init pattern established in Phase 7's map.js, per Phase 8
 * Architecture Discussion (2.4).
 */
let pickerMap = null;
let pickerMarker = null;

function setCoordinates(lat, lon) {
    document.getElementById("latitude").value = Number(lat).toFixed(6);
    document.getElementById("longitude").value = Number(lon).toFixed(6);
}

function initLocationPicker(centerLat, centerLon) {
    pickerMap = L.map("location-picker-map").setView([centerLat, centerLon], 14);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(pickerMap);

    pickerMarker = L.marker([centerLat, centerLon], { draggable: true }).addTo(pickerMap);
    setCoordinates(centerLat, centerLon);

    pickerMarker.on("dragend", (e) => {
        const { lat, lng } = e.target.getLatLng();
        setCoordinates(lat, lng);
    });

    pickerMap.on("click", (e) => {
        pickerMarker.setLatLng(e.latlng);
        setCoordinates(e.latlng.lat, e.latlng.lng);
    });
}

function showAlert(message, isError) {
    const alertBox = document.getElementById("submit-alert");
    alertBox.textContent = message;
    alertBox.className = `alert ${isError ? "alert-danger" : "alert-success"}`;
}

async function submitComplaint() {
    const description = document.getElementById("description").value.trim();
    const latitude = document.getElementById("latitude").value;
    const longitude = document.getElementById("longitude").value;
    const imageInput = document.getElementById("image");

    if (description.length < 10) {
        showAlert("Description must be at least 10 characters.", true);
        return;
    }
    if (!latitude || !longitude) {
        showAlert("Please pin a location on the map.", true);
        return;
    }

    const formData = new FormData();
    formData.append("description", description);
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);
    if (imageInput.files[0]) formData.append("image", imageInput.files[0]);

    const response = await fetch("/api/complaints/", {
        method: "POST",
        headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        body: formData,
    });

    if (response.ok) {
        showAlert("Complaint submitted successfully. Thank you for reporting.", false);
        document.getElementById("description").value = "";
        imageInput.value = "";
    } else {
        const errorData = await response.json();
        showAlert(`Submission failed: ${JSON.stringify(errorData)}`, true);
    }
}

document.getElementById("submit-complaint").addEventListener("click", submitComplaint);

// Center picker on browser geolocation if available, else default
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        (pos) => initLocationPicker(pos.coords.latitude, pos.coords.longitude),
        () => initLocationPicker(33.6844, 73.0479)
    );
} else {
    initLocationPicker(33.6844, 73.0479);
}