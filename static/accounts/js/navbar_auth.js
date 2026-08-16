/**
 * Shared navbar behavior across every page extending dashboard/base.html:
 * shows the logged-in username, wires the logout button, shows the
 * "Manage Complaints" link for authority/admin roles only, and clears
 * JWT tokens from localStorage on logout.
 */
async function initNavbarAuth() {
    const token = localStorage.getItem("access_token");
    const logoutBtn = document.getElementById("logout-btn");
    const usernameLabel = document.getElementById("navbar-username");
    const manageLink = document.getElementById("nav-manage-link");

    if (!token) {
        return; // login/register pages have no token yet — nothing to show
    }

    logoutBtn.classList.remove("d-none");

    try {
        const response = await fetch("/api/auth/me/", {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
            const me = await response.json();
            usernameLabel.textContent = `${me.username} (${me.role})`;
            if (me.role === "authority" || me.role === "admin") {
                manageLink.classList.remove("d-none");
            }
        }
    } catch (err) {
        console.error("Failed to load current user for navbar:", err);
    }

    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login/";
    });
}

initNavbarAuth();