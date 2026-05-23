renderNavbar("Home");

const token =
    localStorage.getItem("token");

const role =
    localStorage.getItem("role");


// ======================================
// HIDE REGISTER BUTTON
// ======================================

if (token) {

    const heroRegisterBtn =

        document.getElementById(
            "heroRegisterBtn"
        );

    if (heroRegisterBtn) {

        heroRegisterBtn.style.display =
            "none";
    }
}


// ======================================
// BOOKING MODAL
// ======================================

const bookingModal =
    document.getElementById(
        "bookingModal"
    );

function openBookingModal() {

    bookingModal.classList.add("active");
}

function closeBookingModal() {

    bookingModal.classList.remove("active");
}

function handleBookingModalClick(event) {

    if (event.target === bookingModal) {

        closeBookingModal();
    }
}


// ======================================
// BOOK EVENT
// ======================================

function bookEvent(eventId) {

    if (!token) {

        showToast(
            "Please login first",
            "error"
        );

        setTimeout(() => {

            window.location.href =
                "login.html";

        }, 1000);

        return;
    }

    if (role === "ORGANISER") {

        showToast(
            "Organisers cannot book events",
            "error"
        );

        return;
    }

    document.getElementById(
        "selectedEventId"
    ).value = eventId;

    openBookingModal();
}


// ======================================
// BOOKING FORM
// ======================================

document.getElementById("bookingForm")
    .addEventListener("submit", function(e) {

        e.preventDefault();

        clearErrors("ticketsError");

        const tickets =
            document.getElementById(
                "numberOfTickets"
            ).value;

        const eventId =
            document.getElementById(
                "selectedEventId"
            ).value;

        if (

            tickets === ""

            ||

            parseInt(tickets) <= 0
        ) {

            setError(

                "ticketsError",

                "Enter valid number of tickets"
            );

            return;
        }

        const bookingData = {

            eventId:
                parseInt(eventId),

            numberOfTickets:
                parseInt(tickets)
        };

        localStorage.setItem(

            "pendingBooking",

            JSON.stringify(bookingData)
        );

        window.location.href =
            "payment.html";
    });


// ======================================
// LOAD EVENTS
// ======================================

async function loadEvents() {

    const eventContainer =

        document.getElementById(
            "eventContainer"
        );

    try {

        const events =
            await getAllEvents();

        eventContainer.innerHTML = "";

        if (events.length === 0) {

            eventContainer.innerHTML = `

                <div class="empty-state">

                    <h3>
                        No Events Yet
                    </h3>

                    <p>
                        Check back soon
                    </p>

                </div>
            `;

            return;
        }

        events.forEach(event => {

            const actionButtons = [

                {
                    label: "Book Now",

                    class: "btn-primary",

                    onclick:
                        `bookEvent(${event.id})`
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
                    Failed to load events.
                </p>

            </div>
        `;
    }
}


// ======================================
// INITIAL LOAD
// ======================================

loadEvents();