document.documentElement.setAttribute("data-theme", localStorage.getItem("theme") || "dark");

document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const role = document.getElementById("role").value;

    clearErrors("nameError", "emailError", "passwordError", "phoneError", "roleError", "registerError");

    let isValid = true;

    if (name === "") {
        setError("nameError", "Name is required");
        isValid = false;
    } else if (name.length < 3) {
        setError("nameError", "Name must be at least 3 characters");
        isValid = false;
    } else if (!/^[A-Za-z ]+$/.test(name)) {
        setError("nameError", "Name can only contain alphabets");
        isValid = false;
    }

    if (email === "") {
        setError("emailError", "Email is required");
        isValid = false;
    } else if (!validateEmail(email)) {
        setError("emailError", "Invalid email format");
        isValid = false;
    }

    const passwordError = validatePassword(password);
    if (password === "") {
        setError("passwordError", "Password is required");
        isValid = false;
    } else if (passwordError) {
        setError("passwordError", passwordError);
        isValid = false;
    }

    if (phone === "") {
        setError("phoneError", "Phone number is required");
        isValid = false;
    } else if (!validatePhone(phone)) {
        setError("phoneError", "Phone must be exactly 10 digits");
        isValid = false;
    }

    if (role === "") {
        setError("roleError", "Please select a role");
        isValid = false;
    }

    if (!isValid) return;

    try {
        const response = await registerUser({ name, email, password, phone, role });
        showToast(response, "success");
        setTimeout(() => window.location.href = "login.html", 1000);
    } catch (error) {
        setError("registerError", error.message);
    }
});
