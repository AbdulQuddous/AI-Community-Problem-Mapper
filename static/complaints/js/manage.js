/**
 * Manage complaints page: lists main complaints with their AI-linked
 * duplicates nested inline, and a quick status toggle. The toggle
 * reuses the existing PATCH /api/complaints/{id}/status/ action from
 * Phase 5 — status stays the full 4-stage lifecycle server-side;
 * this button is just a fast Solved/Unsolved shortcut over it.
 */
if (!localStorage.getItem("access_token")) {
    window.location.href = "/login/";
}

const STATUS_LABELS = {
    received: "Received",
    in_review: "In Review",
    in_progress: "In Progress",
    resolved: "Resolved",
};

const STATUS_BADGE_CLASS = {
    received: "bg-secondary",
    in_review: "bg-primary",
    in_progress: "bg-warning text-dark",
    resolved: "bg-success",
};

function authHeaders() {
    return { Authorization: `Bearer ${localStorage.getItem("access_token")}` };
}

function buildQueryString() {
    const params = new URLSearchParams();
    const category = document.getElementById("filter-category").value;
    const statusFilter = document.getElementById("filter-status").value;
    if (category) params.append("category", category);
    if (statusFilter) params.append("status", statusFilter);
    return params.toString();
}

async function loadManageList() {
    const tbody = document.getElementById("manage-tbody");
    tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">Loading...</td></tr>`;

    const qs = buildQueryString();
    const response = await fetch(`/api/complaints/manage/?${qs}`, { headers: authHeaders() });

    if (response.status === 403) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">You do not have permission to view this page.</td></tr>`;
        return;
    }
    if (!response.ok) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">Failed to load complaints.</td></tr>`;
        return;
    }

    const data = await response.json();
    const complaints = data.results || data;
    renderRows(complaints);
}

function renderRows(complaints) {
    const tbody = document.getElementById("manage-tbody");
    if (complaints.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">No complaints found.</td></tr>`;
        return;
    }

    tbody.innerHTML = "";
    complaints.forEach((c) => {
        const mainRow = document.createElement("tr");
        const badgeClass = STATUS_BADGE_CLASS[c.status] || "bg-secondary";
        const isResolved = c.status === "resolved";
        const toggleLabel = isResolved ? "Mark Unsolved" : "Mark Solved";
        const toggleClass = isResolved ? "btn-outline-secondary" : "btn-success";

        mainRow.innerHTML = `
            <td>${c.category || "<span class='text-muted'>Uncategorized</span>"}</td>
            <td style="max-width: 320px;">${escapeHtml(c.description).slice(0, 100)}${c.description.length > 100 ? "…" : ""}</td>
            <td>${c.user || "-"}</td>
            <td>${c.priority_score ?? "N/A"}</td>
            <td><span class="badge ${badgeClass}">${STATUS_LABELS[c.status] || c.status}</span></td>
            <td>
                ${c.duplicate_count > 0
                    ? `<button class="btn btn-sm btn-link p-0" onclick="toggleDuplicates('${c.id}')">${c.duplicate_count} more report${c.duplicate_count > 1 ? "s" : ""}</button>`
                    : "<span class='text-muted'>—</span>"}
            </td>
            <td>${new Date(c.created_at).toLocaleDateString()}</td>
            <td><button class="btn btn-sm ${toggleClass}" onclick="toggleStatus('${c.id}', '${c.status}', this)">${toggleLabel}</button></td>
        `;
        tbody.appendChild(mainRow);

        if (c.duplicate_count > 0) {
            const dupRow = document.createElement("tr");
            dupRow.id = `duplicates-${c.id}`;
            dupRow.className = "d-none";
            dupRow.innerHTML = `
                <td></td>
                <td colspan="7">
                    <div class="ps-3 border-start border-3">
                        ${c.duplicates.map((d) => `
                            <div class="small text-muted mb-1">
                                <strong>${d.user}</strong> — ${escapeHtml(d.description).slice(0, 80)}
                                <span class="badge ${STATUS_BADGE_CLASS[d.status] || "bg-secondary"} ms-1">${STATUS_LABELS[d.status] || d.status}</span>
                                <span class="ms-1">(${new Date(d.created_at).toLocaleDateString()})</span>
                            </div>
                        `).join("")}
                    </div>
                </td>
            `;
            tbody.appendChild(dupRow);
        }
    });
}

function toggleDuplicates(complaintId) {
    const row = document.getElementById(`duplicates-${complaintId}`);
    if (row) row.classList.toggle("d-none");
}

async function toggleStatus(complaintId, currentStatus, buttonEl) {
    const newStatus = currentStatus === "resolved" ? "received" : "resolved";
    buttonEl.disabled = true;

    const response = await fetch(`/api/complaints/${complaintId}/status/`, {
        method: "PATCH",
        headers: { ...authHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
    });

    if (response.ok) {
        loadManageList();
    } else {
        buttonEl.disabled = false;
        alert("Failed to update status.");
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

document.getElementById("apply-filters").addEventListener("click", loadManageList);

loadManageList();