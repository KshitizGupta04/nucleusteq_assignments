function initTheme() {
    const saved = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", saved);
    return saved;
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    const btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = next === "dark" ? "☀ Light Mode" : "☾ Dark Mode";
}

function renderNavbar(activePage) {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    const theme = initTheme();

    const isOrganiser = role === "ORGANISER";
    const isCustomer = role === "CUSTOMER";

    const navItems = [
        { label: "Home", href: "home.html", show: true, id: "homeNav" },
        { label: "My Bookings", href: "bookings.html", show: !!token && isCustomer, id: "bookingsNav" },
        { label: "Dashboard", href: "dashboard.html", show: !!token && isOrganiser, id: "dashboardNav" },
        { label: "Login", href: "login.html", show: !token, id: "loginNav" },
        { label: "Register", href: "register.html", show: !token, id: "registerNav" },
        { label: "Logout", href: "#", show: !!token, id: "logoutNav", onclick: "logoutUser()" },
    ];

    const linksHtml = navItems
        .filter(item => item.show)
        .map(item => `
            <li>
                <a href="${item.href}"
                   ${item.onclick ? `onclick="${item.onclick}"` : ""}
                   ${item.label === activePage ? 'class="active"' : ""}>
                    ${item.label}
                </a>
            </li>
        `).join("");

    const navbar = document.createElement("nav");
    navbar.className = "navbar";
    navbar.innerHTML = `
        <div class="logo">Eventify</div>
        <div class="nav-right">
            <ul class="nav-links">${linksHtml}</ul>
            <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()">
                ${theme === "dark" ? "☀ Light Mode" : "☾ Dark Mode"}
            </button>
        </div>
    `;

    document.body.insertBefore(navbar, document.body.firstChild);
}

function logoutUser() {
    localStorage.clear();
    window.location.href = "login.html";
}
