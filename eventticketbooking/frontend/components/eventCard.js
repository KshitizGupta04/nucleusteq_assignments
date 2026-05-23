const DEFAULT_EVENT_IMAGE =
    "../assets/concert.png";


// ======================================
// EVENT IMAGE
// ======================================

function getEventImage(imageUrl) {

    return imageUrl &&
    imageUrl.trim() !== ""

        ? imageUrl

        : DEFAULT_EVENT_IMAGE;
}


// ======================================
// EVENT CARD
// ======================================

function renderEventCard({
    event,
    actionButtons
}) {

    return `

        <div class="event-card">

            <div class="event-image-wrapper">

                <img

                    src="${getEventImage(event.imageUrl)}"

                    alt="${event.title}"

                    class="event-image"

                    onerror="this.src='${DEFAULT_EVENT_IMAGE}'"
                >

            </div>

            <div class="event-content">

                <div class="event-top">

                    <h3 class="event-title">

                        ${event.title}

                    </h3>

                    <span class="event-price">

                        ₹${event.price}

                    </span>

                </div>

                <p class="event-description">

                    ${event.description}

                </p>

                <div class="event-details">

                    <div class="event-detail-item">

                        📍 ${event.location}

                    </div>

                    <div class="event-detail-item">

                        📅 ${event.date}

                    </div>

                    <div class="event-detail-item">

                        ⏰ ${event.time}

                    </div>

                    <div class="event-detail-item">

                        🎟 ${event.availableSeats}
                        Seats Left

                    </div>

                </div>

                <div class="event-actions">

                    ${actionButtons.map(button => `

                        <button

                            class="btn ${button.class}"

                            onclick="${button.onclick}"
                        >

                            ${button.label}

                        </button>

                    `).join("")}

                </div>

            </div>

        </div>
    `;
}


// ======================================
// BOOKING CARD
// ======================================

function renderBookingCard(booking) {

    const eventDateTime = new Date(
        `${booking.eventDate}T${booking.eventTime}`
    );

    const isCompleted =
        new Date() > eventDateTime;


    let statusText =
        booking.bookingStatus;

    let statusClass =
        "badge-booked";


    // =====================================
    // COMPLETED EVENT
    // =====================================

    if (

        isCompleted

        &&

        booking.bookingStatus === "BOOKED"
    ) {

        statusText = "COMPLETED";

        statusClass = "badge-completed";
    }


    // =====================================
    // CANCELLED BOOKING
    // =====================================

    if (

        booking.bookingStatus === "CANCELLED"
    ) {

        statusClass = "badge-cancelled";
    }


    // =====================================
    // SHOW CANCEL BUTTON ONLY
    // FOR ACTIVE BOOKINGS
    // =====================================

    const cancelBtn =

        !isCompleted

        &&

        booking.bookingStatus === "BOOKED"

            ? `

                <button

                    class="
                        btn
                        btn-danger
                        cancel-btn
                    "

                    onclick="
                        removeBooking(${booking.id})
                    "
                >

                    Cancel Booking

                </button>
            `

            : "";


    return `

        <div class="booking-card">

            <div class="booking-header">

                <h3>

                    ${booking.eventTitle || `Booking #${booking.id}`}

                </h3>

                <span class="
                    badge
                    ${statusClass}
                ">

                    ${statusText}

                </span>

            </div>

            <div class="booking-details">

                <p>

                    🎫 Event ID:
                    ${booking.eventId}

                </p>

                <p>

                    👥 Tickets:
                    ${booking.numberOfTickets}

                </p>

                <p>

                    📍 Location:
                    ${booking.eventLocation || "N/A"}

                </p>

                <p>

                    📅 Date:
                    ${booking.eventDate || "N/A"}

                </p>

                <p>

                    ⏰ Time:
                    ${booking.eventTime || "N/A"}

                </p>

            </div>

            ${cancelBtn}

        </div>
    `;
}