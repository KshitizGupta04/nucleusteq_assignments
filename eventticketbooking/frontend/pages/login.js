document.documentElement.setAttribute("data-theme", localStorage.getItem("theme") || "dark");

document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    clearErrors("emailError", "passwordError", "loginError");

    let isValid = true;

    if (email === "") {
        setError("emailError", "Email is required");
        isValid = false;
    } else if (!validateEmail(email)) {
        setError("emailError", "Invalid email format");
        isValid = false;
    }

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
        const payload = JSON.parse(atob(response.token.split(".")[1]));

        localStorage.setItem("token", response.token);
        localStorage.setItem("role", payload.role);

        showToast("Login successful!", "success");

        setTimeout(() => {
            window.location.href = payload.role === "ORGANISER" ? "dashboard.html" : "home.html";
        }, 800);
    } catch (error) {
        setError("loginError", error.message);
    }
});
