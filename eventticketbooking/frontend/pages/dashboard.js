renderNavbar("Dashboard");

const token = localStorage.getItem("token");

const role = localStorage.getItem("role");


// ======================================
// AUTH CHECK
// ======================================

if (!token || role !== "ORGANISER") {

    showToast("Access Denied", "error");

    setTimeout(() => {

        window.location.href = "login.html";

    }, 800);
}


// ======================================
// THEME
// ======================================

const theme =
    localStorage.getItem("theme") || "dark";

document.documentElement.setAttribute(
    "data-theme",
    theme
);

const themeBtn =
    document.getElementById("themeToggle");

if (themeBtn) {

    themeBtn.textContent =

        theme === "dark"

            ? "☀ Light Mode"

            : "☾ Dark Mode";
}


// ======================================
// MODALS
// ======================================

const createModal =
    document.getElementById("createEventModal");

const editModal =
    document.getElementById("editEventModal");

const bookingModal =
    document.getElementById("bookingModal");


// ======================================
// MODAL FUNCTIONS
// ======================================

function openCreateModal() {

    createModal.classList.add("active");
}

function closeCreateModal() {

    createModal.classList.remove("active");
}

function openEditModal() {

    editModal.classList.add("active");
}

function closeEditModal() {

    editModal.classList.remove("active");
}

function openBookingModal() {

    bookingModal.classList.add("active");
}

function closeBookingModal() {

    bookingModal.classList.remove("active");
}

function handleModalClick(event) {

    if (event.target === createModal) {

        closeCreateModal();
    }
}

function handleEditModalClick(event) {

    if (event.target === editModal) {

        closeEditModal();
    }
}

function handleBookingModalClick(event) {

    if (event.target === bookingModal) {

        closeBookingModal();
    }
}


// ======================================
// VALIDATION HELPERS
// ======================================

function validateTime(time) {

    return /^\d{2}:\d{2}$/.test(time);
}

function validateImage(image) {

    if (!image) return true;

    const allowedTypes = [

        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp"
    ];

    return allowedTypes.includes(image.type);
}


// ======================================
// LOAD EVENTS
// ======================================

async function loadEvents() {

    const eventContainer =
        document.getElementById("eventContainer");

    try {

        const events =
            await getMyEvents();

        eventContainer.innerHTML = "";

        if (events.length === 0) {

            eventContainer.innerHTML = `

                <div class="empty-state">

                    <h3>
                        No Events Created
                    </h3>

                    <p>
                        Create your first event
                    </p>

                </div>
            `;

            return;
        }

        events.forEach(event => {

            const actionButtons = [

                {
                    label: "Edit",
                    class: "btn-outline",
                    onclick: `editEvent(${event.id})`
                },

                {
                    label: "Bookings",
                    class: "btn-secondary",
                    onclick: `viewBookings(${event.id})`
                },

                {
                    label: "Delete",
                    class: "btn-danger",
                    onclick: `removeEvent(${event.id})`
                }
            ];

            eventContainer.innerHTML +=

                renderEventCard({

                    event,

                    actionButtons
                });
        });

    } catch (error) {

        eventContainer.innerHTML = `

            <div class="error-state">

                <p>
                    Failed to load events
                </p>

            </div>
        `;
    }
}


// ======================================
// CREATE EVENT
// ======================================

document.getElementById("eventForm")
    .addEventListener("submit", async function(e) {

        e.preventDefault();

        clearErrors(

            "titleError",
            "descriptionError",
            "locationError",
            "dateError",
            "timeError",
            "priceError",
            "seatsError",
            "imageError"
        );

        const title =
            document.getElementById("title")
                .value.trim();

        const description =
            document.getElementById("description")
                .value.trim();

        const location =
            document.getElementById("location")
                .value.trim();

        const date =
            document.getElementById("date")
                .value;

        const time =
            document.getElementById("time")
                .value;

        const price =
            document.getElementById("price")
                .value;

        const seats =
            document.getElementById("availableSeats")
                .value;

        const image =
            document.getElementById("image")
                .files[0];

        let isValid = true;


        if (title.length < 3) {

            setError(
                "titleError",
                "Title must be at least 3 characters"
            );

            isValid = false;
        }

        if (description.length < 10) {

            setError(
                "descriptionError",
                "Description must be at least 10 characters"
            );

            isValid = false;
        }

        if (location.length < 3) {

            setError(
                "locationError",
                "Location must be at least 3 characters"
            );

            isValid = false;
        }

        if (date === "") {

            setError(
                "dateError",
                "Date is required"
            );

            isValid = false;
        }

        if (!validateTime(time)) {

            setError(
                "timeError",
                "Time must be HH:mm"
            );

            isValid = false;
        }

        if (price <= 0) {

            setError(
                "priceError",
                "Price must be greater than 0"
            );

            isValid = false;
        }

        if (seats <= 0) {

            setError(
                "seatsError",
                "Seats must be greater than 0"
            );

            isValid = false;
        }

        if (!validateImage(image)) {

            setError(
                "imageError",
                "Only PNG/JPG/JPEG/WEBP allowed"
            );

            isValid = false;
        }

        if (!isValid) return;


        const formData =
            new FormData();

        formData.append("title", title);

        formData.append("description", description);

        formData.append("location", location);

        formData.append("date", date);

        formData.append("time", time);

        formData.append("price", price);

        formData.append("availableSeats", seats);

        if (image) {

            formData.append("image", image);
        }

        try {

            const response =
                await createEvent(formData);

            showToast(response, "success");

            closeCreateModal();

            this.reset();

            loadEvents();

        } catch (error) {

            showToast(error.message, "error");
        }
    });


// ======================================
// EDIT EVENT
// ======================================

async function editEvent(id) {

    try {

        const event =
            await getEventById(id);

        document.getElementById(
            "editEventId"
        ).value = event.id;

        document.getElementById(
            "editTitle"
        ).value = event.title;

        document.getElementById(
            "editDescription"
        ).value = event.description;

        document.getElementById(
            "editLocation"
        ).value = event.location;

        document.getElementById(
            "editDate"
        ).value = event.date;

        document.getElementById(
            "editTime"
        ).value = event.time;

        document.getElementById(
            "editPrice"
        ).value = event.price;

        document.getElementById(
            "editAvailableSeats"
        ).value = event.availableSeats;

        openEditModal();

    } catch (error) {

        showToast(error.message, "error");
    }
}


// ======================================
// UPDATE EVENT
// ======================================

document.getElementById("editEventForm")
    .addEventListener("submit", async function(e) {

        e.preventDefault();

        clearErrors(

            "editTitleError",
            "editDescriptionError",
            "editLocationError",
            "editDateError",
            "editTimeError",
            "editPriceError",
            "editSeatsError",
            "editImageError"
        );

        const id =
            document.getElementById(
                "editEventId"
            ).value;

        const title =
            document.getElementById(
                "editTitle"
            ).value.trim();

        const description =
            document.getElementById(
                "editDescription"
            ).value.trim();

        const location =
            document.getElementById(
                "editLocation"
            ).value.trim();

        const date =
            document.getElementById(
                "editDate"
            ).value;

        const time =
            document.getElementById(
                "editTime"
            ).value;

        const price =
            document.getElementById(
                "editPrice"
            ).value;

        const seats =
            document.getElementById(
                "editAvailableSeats"
            ).value;

        const image =
            document.getElementById(
                "editImage"
            ).files[0];

        let isValid = true;


        if (title.length < 3) {

            setError(
                "editTitleError",
                "Title must be at least 3 characters"
            );

            isValid = false;
        }

        if (description.length < 10) {

            setError(
                "editDescriptionError",
                "Description must be at least 10 characters"
            );

            isValid = false;
        }

        if (location.length < 3) {

            setError(
                "editLocationError",
                "Location must be at least 3 characters"
            );

            isValid = false;
        }

        if (date === "") {

            setError(
                "editDateError",
                "Date is required"
            );

            isValid = false;
        }

        if (!validateTime(time)) {

            setError(
                "editTimeError",
                "Time must be HH:mm"
            );

            isValid = false;
        }

        if (price <= 0) {

            setError(
                "editPriceError",
                "Price must be greater than 0"
            );

            isValid = false;
        }

        if (seats <= 0) {

            setError(
                "editSeatsError",
                "Seats must be greater than 0"
            );

            isValid = false;
        }

        if (!validateImage(image)) {

            setError(
                "editImageError",
                "Only PNG/JPG/JPEG/WEBP allowed"
            );

            isValid = false;
        }

        if (!isValid) return;


        const formData =
            new FormData();

        formData.append("title", title);

        formData.append("description", description);

        formData.append("location", location);

        formData.append("date", date);

        formData.append("time", time);

        formData.append("price", price);

        formData.append("availableSeats", seats);

        if (image) {

            formData.append("image", image);
        }

        try {

            const response =
                await updateEvent(id, formData);

            showToast(response, "success");

            closeEditModal();

            loadEvents();

        } catch (error) {

            showToast(error.message, "error");
        }
    });


// ======================================
// DELETE EVENT
// ======================================

async function removeEvent(id) {

    if (!confirm(
        "Delete this event?"
    )) {

        return;
    }

    try {

        const response =
            await deleteEvent(id);

        showToast(response, "success");

        loadEvents();

    } catch (error) {

        showToast(error.message, "error");
    }
}


// ======================================
// VIEW BOOKINGS
// ======================================

async function viewBookings(eventId) {

    const bookingModalBody =
        document.getElementById(
            "bookingModalBody"
        );

    try {

        const bookings =
            await getBookingsForEvent(eventId);

        bookingModalBody.innerHTML = "";

        if (bookings.length === 0) {

            bookingModalBody.innerHTML = `

                <p>
                    No bookings yet
                </p>
            `;

            openBookingModal();

            return;
        }

        bookings.forEach(booking => {

            bookingModalBody.innerHTML += `

                <div class="booking-row">

                    <p>

                        <strong>Email:</strong>

                        ${booking.customerEmail}

                    </p>

                    <p>

                        <strong>Tickets:</strong>

                        ${booking.numberOfTickets}

                    </p>

                    <p>

                        <strong>Status:</strong>

                        ${booking.bookingStatus}

                    </p>

                    <hr>

                </div>
            `;
        });

        openBookingModal();

    } catch (error) {

        showToast(error.message, "error");
    }
}


// ======================================
// SEARCH EVENTS
// ======================================

document.getElementById("searchInput")
    .addEventListener("input", async function() {

        const query =
            this.value.toLowerCase();

        const eventContainer =
            document.getElementById(
                "eventContainer"
            );

        try {

            const events =
                await getMyEvents();

            const filteredEvents =
                events.filter(event =>

                    event.title
                        .toLowerCase()
                        .includes(query)
                );

            eventContainer.innerHTML = "";

            if (filteredEvents.length === 0) {

                eventContainer.innerHTML = `

                    <div class="empty-state">

                        <h3>
                            No matching events
                        </h3>

                    </div>
                `;

                return;
            }

            filteredEvents.forEach(event => {

                const actionButtons = [

                    {
                        label: "Edit",
                        class: "btn-outline",
                        onclick: `editEvent(${event.id})`
                    },

                    {
                        label: "Bookings",
                        class: "btn-secondary",
                        onclick: `viewBookings(${event.id})`
                    },

                    {
                        label: "Delete",
                        class: "btn-danger",
                        onclick: `removeEvent(${event.id})`
                    }
                ];

                eventContainer.innerHTML +=

                    renderEventCard({

                        event,

                        actionButtons
                    });
            });

        } catch (error) {

            showToast(
                "Search failed",
                "error"
            );
        }
    });


// ======================================
// INITIAL LOAD
// ======================================

loadEvents();