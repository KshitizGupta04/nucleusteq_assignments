renderNavbar("Home");

const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

if (token) {
    const heroRegisterBtn = document.getElementById("heroRegisterBtn");
    if (heroRegisterBtn) heroRegisterBtn.style.display = "none";
}

function bookEvent(eventId) {
    if (!token) {
        showToast("Please login first", "error");
        setTimeout(() => window.location.href = "login.html", 1000);
        return;
    }

    if (role === "ORGANISER") {
        showToast("Organisers cannot book events", "error");
        return;
    }

    window.location.href = `bookings.html?eventId=${eventId}`;
}

async function loadEvents() {
    const eventContainer = document.getElementById("eventContainer");

    try {
        const events = await getAllEvents();
        eventContainer.innerHTML = "";

        if (events.length === 0) {
            eventContainer.innerHTML = `<div class="empty-state"><h3>No Events Yet</h3><p>Check back soon for upcoming events</p></div>`;
            return;
        }

        events.forEach(event => {
            const actionButtons = [{
                label: "Book Now",
                class: "btn-primary",
                onclick: `bookEvent(${event.id})`
            }];

            eventContainer.innerHTML += renderEventCard({ event, actionButtons });
        });
    } catch (error) {
        eventContainer.innerHTML = `<div class="error-state"><p>Failed to load events. Please try again.</p></div>`;
    }
}

loadEvents();
