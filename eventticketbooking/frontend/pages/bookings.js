const token = localStorage.getItem("token");
const role = localStorage.getItem("role");
const theme = localStorage.getItem("theme") || "dark";

document.documentElement.setAttribute("data-theme", theme);

const themeBtn = document.getElementById("themeToggle");
if (themeBtn) themeBtn.textContent = theme === "dark" ? "☀ Light Mode" : "☾ Dark Mode";

if (!token || role !== "CUSTOMER") {
    showToast("Access Denied", "error");
    setTimeout(() => window.location.href = "login.html", 800);
}

const params = new URLSearchParams(window.location.search);
const eventId = params.get("eventId");

document.getElementById("bookingForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const numberOfTickets = document.getElementById("numberOfTickets").value;

    clearErrors("ticketsError");

    if (numberOfTickets === "" || !validatePositiveInteger(numberOfTickets)) {
        setError("ticketsError", "Enter a valid number of tickets (min 1)");
        return;
    }

    if (!eventId) {
        showToast("No event selected. Go back and choose an event.", "error");
        return;
    }

    const bookingData = {
        eventId: parseInt(eventId),
        numberOfTickets: parseInt(numberOfTickets)
    };

    try {
        const response = await bookTickets(bookingData);
        showToast(response, "success");
        document.getElementById("bookingForm").reset();
        loadBookings();
    } catch (error) {
        showToast(error.message, "error");
    }
});

async function loadBookings() {
    const bookingContainer = document.getElementById("bookingContainer");

    try {
        const bookings = await getMyBookings();
        bookingContainer.innerHTML = "";

        if (bookings.length === 0) {
            bookingContainer.innerHTML = `<div class="empty-state"><h3>No Bookings Yet</h3><p>Book an event to see it here</p></div>`;
            return;
        }

        bookings.forEach(booking => {
            bookingContainer.innerHTML += renderBookingCard(booking);
        });
    } catch (error) {
        bookingContainer.innerHTML = `<div class="error-state"><p>Failed to load bookings.</p></div>`;
    }
}

async function removeBooking(id) {
    if (!confirm("Cancel this booking?")) return;

    try {
        const response = await cancelBooking(id);
        showToast(response, "success");
        loadBookings();
    } catch (error) {
        showToast(error.message, "error");
    }
}

loadBookings();
