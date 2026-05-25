(function () {

    const savedTheme =

        localStorage.getItem("theme")

        ||

        "dark";

    document.documentElement.setAttribute(

        "data-theme",

        savedTheme
    );

})();


function updateThemeButton() {

    const btn =

        document.getElementById(
            "themeToggle"
        );

    if (!btn) return;

    const currentTheme =

        document.documentElement.getAttribute(
            "data-theme"
        );

    btn.textContent =

        currentTheme === "dark"

            ? "☀ Light Mode"

            : "☾ Dark Mode";
}


function toggleTheme() {

    const current =

        document.documentElement.getAttribute(
            "data-theme"
        );

    const next =

        current === "dark"

            ? "light"

            : "dark";

    document.documentElement.setAttribute(
        "data-theme",
        next
    );

    localStorage.setItem(
        "theme",
        next
    );

    updateThemeButton();
}


function renderNavbar(activePage) {

    const token =
        localStorage.getItem("token");

    const role =
        localStorage.getItem("role");

    const currentTheme =
        localStorage.getItem("theme")
        || "dark";

    const isOrganiser =
        role === "ORGANISER";

    const isCustomer =
        role === "CUSTOMER";

    const navItems = [

        {
            label: "Home",
            href: "home.html",
            show: true
        },

        {
            label: "My Bookings",
            href: "bookings.html",
            show: !!token && isCustomer
        },

        {
            label: "Dashboard",
            href: "dashboard.html",
            show: !!token && isOrganiser
        },

        {
            label: "Login",
            href: "login.html",
            show: !token
        },

        {
            label: "Register",
            href: "register.html",
            show: !token
        },

        {
            label: "Logout",
            href: "#",
            show: !!token,
            onclick: "logoutUser()"
        }
    ];

    const linksHtml = navItems

        .filter(item => item.show)

        .map(item => `

            <li>

                <a

                    href="${item.href}"

                    ${item.onclick
                        ? `onclick="${item.onclick}"`
                        : ""
                    }

                    ${item.label === activePage
                        ? 'class="active"'
                        : ""
                    }
                >

                    ${item.label}

                </a>

            </li>

        `)

        .join("");

    const navbar =
        document.createElement("nav");

    navbar.className =
        "navbar";

    navbar.innerHTML = `

        <div class="logo">

            Eventify

        </div>

        <div class="nav-right">

            <ul class="nav-links">

                ${linksHtml}

            </ul>

            <button

                class="theme-toggle"

                id="themeToggle"

                onclick="toggleTheme()"
            >

                ${currentTheme === "dark"

                    ? "☀ Light Mode"

                    : "☾ Dark Mode"
                }

            </button>

        </div>
    `;

    document.body.insertBefore(

        navbar,

        document.body.firstChild
    );

    updateThemeButton();
}


function logoutUser() {

    localStorage.clear();

    window.location.href =
        "login.html";
}