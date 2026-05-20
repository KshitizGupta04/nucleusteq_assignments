const DEFAULT_EVENT_IMAGE = "../assets/concert.png";

function getEventImage(imageUrl) {
    return imageUrl && imageUrl.trim() !== "" ? imageUrl : DEFAULT_EVENT_IMAGE;
}

function renderEventCard({ event, showActions = true, actionButtons = [] }) {
    const imgSrc = getEventImage(event.imageUrl);

    const actionsHtml = showActions && actionButtons.length > 0
        ? `<div class="event-actions">${actionButtons.map(btn =>
            `<button class="btn ${btn.class}" onclick="${btn.onclick}">${btn.label}</button>`
        ).join("")}</div>`
        : "";

    return `
        <div class="event-card">
            <img src="${imgSrc}" alt="${event.title}" onerror="this.src='${DEFAULT_EVENT_IMAGE}'">
            <div class="event-content">
                <h3>${event.title}</h3>
                ${event.description ? `<p class="description">${event.description}</p>` : ""}
                <p>📍 ${event.location}</p>
                <p>📅 ${event.date} &nbsp; ⏰ ${event.time}</p>
                <p class="price">₹ ${event.price}</p>
                <p>${event.availableSeats} seats available</p>
                ${actionsHtml}
            </div>
        </div>
    `;
}

function renderBookingCard(booking) {
    const statusClass = booking.bookingStatus === "BOOKED" ? "badge-booked" : "badge-cancelled";
    const cancelBtn = booking.bookingStatus === "BOOKED"
        ? `<button class="btn btn-danger cancel-btn" onclick="removeBooking(${booking.id})">Cancel Booking</button>`
        : "";

    return `
        <div class="booking-card">
            <h3>Booking #${booking.id}</h3>
            <p>Event ID: ${booking.eventId}</p>
            <p>Tickets: ${booking.numberOfTickets}</p>
            <p>Status: <span class="badge ${statusClass}">${booking.bookingStatus}</span></p>
            ${cancelBtn}
        </div>
    `;
}
