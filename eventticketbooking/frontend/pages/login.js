document.documentElement.setAttribute(
    "data-theme",
    localStorage.getItem("theme") || "dark"
);

// SHOW/HIDE PASSWORD
function togglePassword() {
    const passwordInput = document.getElementById("password");
    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}

document.getElementById("loginForm")
    .addEventListener("submit", async function (e) {

        e.preventDefault();

        const email    = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        clearErrors("emailError", "passwordError", "loginError");

        let isValid = true;

        // EMAIL
        if (email === "") {
            setError("emailError", "Email is required");
            isValid = false;
        } else if (!validateEmail(email)) {
            setError("emailError", "Invalid email format");
            isValid = false;
        }

        // PASSWORD
        if (password === "") {
            setError("passwordError", "Password is required");
            isValid = false;
        } else if (password.length < 6) {
            setError("passwordError", "Password must be at least 6 characters");
            isValid = false;
        }

        if (!isValid) return;

        try {
            const response = await loginUser({ email, password });

            // DECODE JWT to get role
            const payload = JSON.parse(atob(response.token.split(".")[1]));

            localStorage.setItem("token", response.token);
            localStorage.setItem("role", payload.role);

            showToast("Login successful!", "success");

            setTimeout(() => {
                window.location.href =
                    payload.role === "ORGANISER"
                        ? "dashboard.html"
                        : "home.html";
            }, 800);

        } catch (error) {
            // Show clean message, not raw JSON
            let message = error.message;
            try {
                const parsed = JSON.parse(message);
                message = parsed.message || "Login failed";
            } catch (_) {
                // already a plain string
            }
            setError("loginError", message);
        }
    });