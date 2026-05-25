const BOOKING_URL =
    "http://localhost:8082/api/v1/bookings";

// AUTH HEADERS
function getBookingHeaders() {

    const token =
        localStorage.getItem("token");

    return {

        "Content-Type":
            "application/json",

        "Authorization":
            `Bearer ${token}`
    };
}

// HANDLE ERROR RESPONSE
async function handleBookingError(response) {

    // TOKEN EXPIRED / INVALID
    if (

        response.status === 401

        ||

        response.status === 403
    ) {

        localStorage.clear();

        localStorage.setItem(

            "sessionExpired",

            "true"
        );

        window.location.href =
            "login.html";

        return;
    }


    // OTHER ERRORS
    let errorMessage =
        "Something went wrong";

    try {

        const errorData =
            await response.json();

        errorMessage =

            errorData.message

            ||

            errorMessage;

    } catch (e) {

        // ignore parse error
    }

    throw new Error(errorMessage);
}

// BOOK TICKETS
async function bookTickets(data) {

    const response = await fetch(

        BOOKING_URL,

        {
            method: "POST",

            headers:
                getBookingHeaders(),

            body:
                JSON.stringify(data)
        }
    );

    // HANDLE ERROR
    if (!response.ok) {

        await handleBookingError(
            response
        );
    }

    return await response.text();
}

// MY BOOKINGS
async function getMyBookings() {

    const response = await fetch(

        `${BOOKING_URL}/my-bookings`,

        {
            headers:
                getBookingHeaders()
        }
    );

    if (!response.ok) {

        await handleBookingError(
            response
        );
    }

    return await response.json();
}

// CANCEL BOOKING
async function cancelBooking(id) {

    const response = await fetch(

        `${BOOKING_URL}/${id}`,

        {
            method: "DELETE",

            headers:
                getBookingHeaders()
        }
    );

    if (!response.ok) {

        await handleBookingError(
            response
        );
    }

    return await response.text();
}


// ======================================
// GET BOOKINGS FOR EVENT
// ======================================

async function getBookingsForEvent(eventId) {

    const response = await fetch(

        `${BOOKING_URL}/event/${eventId}`,

        {
            headers:
                getBookingHeaders()
        }
    );

    if (!response.ok) {

        await handleBookingError(
            response
        );
    }

    return await response.json();
}