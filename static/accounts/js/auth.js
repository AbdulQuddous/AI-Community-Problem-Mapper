/**
 * Handles login/register form submission, stores JWT tokens, and
 * redirects based on the authenticated user's role (fetched from
 * /api/auth/me/ right after login — see Phase 4's MeView).
 */
function showAlert(elementId, message, isError) {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.className = `alert ${isError ? "alert-danger" : "alert-success"}`;
}

async function handleLogin() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const response = await fetch("/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        showAlert("login-alert", "Invalid username or password.", true);
        return;
    }

    const data = await response.json();
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);

    const meResponse = await fetch("/api/auth/me/", {
        headers: { Authorization: `Bearer ${data.access}` },
    });
    const me = await meResponse.json();

    if (me.role === "authority" || me.role === "admin") {
        window.location.href = "/dashboard/";
    } else {
        window.location.href = "/complaints/submit/";
    }
}

async function handleRegister() {
    const username = document.getElementById("reg-username").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;
    const password_confirm = document.getElementById("reg-password-confirm").value;

    const response = await fetch("/api/auth/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password, password_confirm }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        showAlert("register-alert", JSON.stringify(errorData), true);
        return;
    }

    showAlert("register-alert", "Account created. Redirecting to login...", false);
    setTimeout(() => (window.location.href = "/login/"), 1200);
}

const loginBtn = document.getElementById("login-btn");
if (loginBtn) loginBtn.addEventListener("click", handleLogin);

const registerBtn = document.getElementById("register-btn");
if (registerBtn) registerBtn.addEventListener("click", handleRegister);