const BOOKING_URL =
    "http://localhost:8082/api/v1/bookings";

function getBookingHeaders() {

    const token = localStorage.getItem("token");

    return {

        "Content-Type": "application/json",

        "Authorization": `Bearer ${token}`
    };
}


// ======================================
// BOOK TICKETS
// ======================================

async function bookTickets(data) {

    const response = await fetch(

        BOOKING_URL,

        {
            method: "POST",

            headers: getBookingHeaders(),

            body: JSON.stringify(data)
        }
    );

    const message = await response.text();

    if (!response.ok) {

        throw new Error(message);
    }

    return message;
}


// ======================================
// MY BOOKINGS
// ======================================

async function getMyBookings() {

    const response = await fetch(

        `${BOOKING_URL}/my-bookings`,

        {
            headers: getBookingHeaders()
        }
    );

    if (!response.ok) {

        throw new Error(
            "Failed to load bookings"
        );
    }

    return await response.json();
}


// ======================================
// CANCEL BOOKING
// ======================================

async function cancelBooking(id) {

    const response = await fetch(

        `${BOOKING_URL}/${id}`,

        {
            method: "DELETE",

            headers: getBookingHeaders()
        }
    );

    const message = await response.text();

    if (!response.ok) {

        throw new Error(message);
    }

    return message;
}


// ======================================
// GET BOOKINGS FOR EVENT
// ======================================

async function getBookingsForEvent(eventId) {

    const response = await fetch(

        `${BOOKING_URL}/event/${eventId}`,

        {
            headers: getBookingHeaders()
        }
    );

    if (!response.ok) {

        throw new Error(
            "Failed to load bookings"
        );
    }

    return await response.json();
}