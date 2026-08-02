/**
 * Loads /api/dashboard/stats/ and renders the summary cards + Chart.js
 * charts. Reads the JWT access token from localStorage (set at login,
 * see Phase 4) and sends it as a Bearer token on every fetch — the
 * dashboard's own request/response cycle relies on the same auth
 * mechanism as the rest of the API, per Phase 4's "stateless JWT for
 * all consumers" decision.
 */
let categoryChart = null;
let trendChart = null;

function getAccessToken() {
    return localStorage.getItem("access_token");
}

function buildQueryString() {
    const params = new URLSearchParams();
    const category = document.getElementById("filter-category").value;
    const dateFrom = document.getElementById("filter-date-from").value;
    const dateTo = document.getElementById("filter-date-to").value;
    if (category) params.append("category", category);
    if (dateFrom) params.append("date_from", dateFrom);
    if (dateTo) params.append("date_to", dateTo);
    return params.toString();
}

async function loadStats() {
    const qs = buildQueryString();
    const response = await fetch(`/api/dashboard/stats/?${qs}`, {
        headers: { Authorization: `Bearer ${getAccessToken()}` },
    });
    if (!response.ok) {
        console.error("Failed to load dashboard stats:", response.status);
        return;
    }
    const data = await response.json();
    renderSummary(data.summary);
    renderCategoryChart(data.category_breakdown);
    renderTrendChart(data.daily_trend);
}

function renderSummary(summary) {
    document.getElementById("stat-total").textContent = summary.total_complaints;
    document.getElementById("stat-unresolved").textContent = summary.unresolved_count;
    document.getElementById("stat-avg-priority").textContent =
        summary.average_priority ? summary.average_priority.toFixed(1) : "N/A";
}

function renderCategoryChart(breakdown) {
    const ctx = document.getElementById("chart-category");
    const labels = breakdown.map((b) => b.category);
    const counts = breakdown.map((b) => b.count);
    if (categoryChart) categoryChart.destroy();
    categoryChart = new Chart(ctx, {
        type: "bar",
        data: { labels, datasets: [{ label: "Complaints", data: counts, backgroundColor: "#0d6efd" }] },
        options: { responsive: true, plugins: { legend: { display: false } } },
    });
}

function renderTrendChart(trend) {
    const ctx = document.getElementById("chart-trend");
    const labels = trend.map((t) => t.day);
    const counts = trend.map((t) => t.count);
    if (trendChart) trendChart.destroy();
    trendChart = new Chart(ctx, {
        type: "line",
        data: { labels, datasets: [{ label: "Complaints per day", data: counts, borderColor: "#198754", fill: false }] },
        options: { responsive: true },
    });
}

document.getElementById("apply-filters").addEventListener("click", () => {
    loadStats();
    if (typeof loadHotspots === "function") loadHotspots();
});

loadStats();