const token = localStorage.getItem("token");
const role = localStorage.getItem("role");
const theme = localStorage.getItem("theme") || "dark";

document.documentElement.setAttribute("data-theme", theme);

const themeBtn = document.getElementById("themeToggle");
if (themeBtn) themeBtn.textContent = theme === "dark" ? "☀ Light Mode" : "☾ Dark Mode";

if (!token || role !== "ORGANISER") {
    showToast("Access Denied", "error");
    setTimeout(() => window.location.href = "login.html", 800);
}

async function loadEvents() {
    const eventContainer = document.getElementById("eventContainer");

    try {
        const events = await getAllEvents();
        eventContainer.innerHTML = "";

        if (events.length === 0) {
            eventContainer.innerHTML = `<div class="empty-state"><h3>No Events Yet</h3><p>Create your first event using the form</p></div>`;
            return;
        }

        events.forEach(event => {
            const actionButtons = [
                { label: "Update", class: "btn-blue", onclick: `editEvent(${event.id})` },
                { label: "Delete", class: "btn-danger", onclick: `removeEvent(${event.id})` }
            ];
            eventContainer.innerHTML += renderEventCard({ event, actionButtons });
        });
    } catch (error) {
        eventContainer.innerHTML = `<div class="error-state"><p>Failed to load events.</p></div>`;
    }
}

document.getElementById("eventForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const location = document.getElementById("location").value.trim();
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value.trim();
    const price = document.getElementById("price").value;
    const availableSeats = document.getElementById("availableSeats").value;
    const imageUrl = document.getElementById("imageUrl").value.trim();

    clearErrors("titleError", "descriptionError", "locationError", "dateError", "timeError", "priceError", "seatsError", "imageError");

    let isValid = true;

    if (title === "") {
        setError("titleError", "Title is required");
        isValid = false;
    } else if (title.length < 3) {
        setError("titleError", "Title must be at least 3 characters");
        isValid = false;
    }

    if (description === "") {
        setError("descriptionError", "Description is required");
        isValid = false;
    } else if (description.length < 10) {
        setError("descriptionError", "Description must be at least 10 characters");
        isValid = false;
    }

    if (location === "") {
        setError("locationError", "Location is required");
        isValid = false;
    }

    if (date === "") {
        setError("dateError", "Date is required");
        isValid = false;
    } else if (new Date(date) < new Date()) {
        setError("dateError", "Date cannot be in the past");
        isValid = false;
    }

    if (time === "") {
        setError("timeError", "Time is required");
        isValid = false;
    }

    if (price === "" || !validatePositiveNumber(price)) {
        setError("priceError", "Enter a valid price");
        isValid = false;
    }

    if (availableSeats === "" || !validatePositiveInteger(availableSeats)) {
        setError("seatsError", "Enter a valid seat count");
        isValid = false;
    }

    if (imageUrl !== "" && !validateImageUrl(imageUrl)) {
        setError("imageError", "Enter a valid image URL (jpg, png, webp)");
        isValid = false;
    }

    if (!isValid) return;

    const eventData = {
        title, description, location, date, time,
        price: parseFloat(price),
        availableSeats: parseInt(availableSeats),
        imageUrl: imageUrl || ""
    };

    try {
        const response = await createEvent(eventData);
        showToast(response, "success");
        document.getElementById("eventForm").reset();
        loadEvents();
    } catch (error) {
        showToast(error.message, "error");
    }
});

async function removeEvent(id) {
    if (!confirm("Delete this event?")) return;

    try {
        const response = await deleteEvent(id);
        showToast(response, "success");
        loadEvents();
    } catch (error) {
        showToast(error.message, "error");
    }
}

async function editEvent(id) {
    try {
        const event = await getEventById(id);

        const title = prompt("Title", event.title);
        if (title === null) return;
        const description = prompt("Description", event.description);
        if (description === null) return;
        const location = prompt("Location", event.location);
        if (location === null) return;
        const date = prompt("Date (YYYY-MM-DD)", event.date);
        if (date === null) return;
        const time = prompt("Time", event.time);
        if (time === null) return;
        const price = prompt("Price", event.price);
        if (price === null) return;
        const availableSeats = prompt("Available Seats", event.availableSeats);
        if (availableSeats === null) return;
        const imageUrl = prompt("Image URL (leave blank to keep)", event.imageUrl || "");
        if (imageUrl === null) return;

        if (!title.trim() || !location.trim() || !date.trim() || !time.trim()) {
            showToast("Title, location, date and time are required", "error");
            return;
        }

        if (isNaN(parseFloat(price)) || parseFloat(price) < 0) {
            showToast("Invalid price", "error");
            return;
        }

        if (isNaN(parseInt(availableSeats)) || parseInt(availableSeats) < 1) {
            showToast("Invalid seat count", "error");
            return;
        }

        const updatedEvent = {
            title: title.trim(),
            description: description.trim(),
            location: location.trim(),
            date: date.trim(),
            time: time.trim(),
            price: parseFloat(price),
            availableSeats: parseInt(availableSeats),
            imageUrl: imageUrl.trim()
        };

        const response = await updateEvent(id, updatedEvent);
        showToast(response, "success");
        loadEvents();
    } catch (error) {
        showToast(error.message, "error");
    }
}

loadEvents();
