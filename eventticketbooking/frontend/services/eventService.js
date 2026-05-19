const EVENT_URL =
    "http://localhost:8082/api/v1/events";

const BOOKING_URL =
    "http://localhost:8082/api/v1/bookings";

// GET TOKEN
function getToken() {

    return localStorage.getItem(
        "token"
    );
}

// GET ALL EVENTS
async function getAllEvents() {

    const response = await fetch(
        EVENT_URL
    );

    if(!response.ok) {

        throw new Error(
            "Failed to fetch events"
        );
    }

    return await response.json();
}

// GET EVENT BY ID
async function getEventById(id) {

    const response = await fetch(

        `${EVENT_URL}/${id}`
    );

    if(!response.ok) {

        throw new Error(
            "Event not found"
        );
    }

    return await response.json();
}

// CREATE EVENT
async function createEvent(eventData) {

    const response = await fetch(

        EVENT_URL,

        {
            method: "POST",

            headers: {

                "Content-Type":
                    "application/json",

                "Authorization":
                    `Bearer ${getToken()}`
            },

            body: JSON.stringify(
                eventData
            )
        }
    );

    if(!response.ok) {

        const error =
            await response.text();

        throw new Error(error);
    }

    return await response.text();
}

// UPDATE EVENT
async function updateEvent(

    id,

    eventData

) {

    const response = await fetch(

        `${EVENT_URL}/${id}`,

        {
            method: "PUT",

            headers: {

                "Content-Type":
                    "application/json",

                "Authorization":
                    `Bearer ${getToken()}`
            },

            body: JSON.stringify(
                eventData
            )
        }
    );

    if(!response.ok) {

        const error =
            await response.text();

        throw new Error(error);
    }

    return await response.text();
}

// DELETE EVENT
async function deleteEvent(id) {

    const response = await fetch(

        `${EVENT_URL}/${id}`,

        {
            method: "DELETE",

            headers: {

                "Authorization":
                    `Bearer ${getToken()}`
            }
        }
    );

    if(!response.ok) {

        const error =
            await response.text();

        throw new Error(error);
    }

    return await response.text();
}

// BOOK EVENT
async function bookEvent(bookingData) {

    const response = await fetch(

        BOOKING_URL,

        {
            method: "POST",

            headers: {

                "Content-Type":
                    "application/json",

                "Authorization":
                    `Bearer ${getToken()}`
            },

            body: JSON.stringify(
                bookingData
            )
        }
    );

    if(!response.ok) {

        const error =
            await response.text();

        throw new Error(error);
    }

    return await response.text();
}

// GET MY BOOKINGS
async function getMyBookings() {

    const response = await fetch(

        `${BOOKING_URL}/my-bookings`,

        {
            headers: {

                "Authorization":
                    `Bearer ${getToken()}`
            }
        }
    );

    if(!response.ok) {

        throw new Error(
            "Failed to fetch bookings"
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

            headers: {

                "Authorization":
                    `Bearer ${getToken()}`
            }
        }
    );

    if(!response.ok) {

        const error =
            await response.text();

        throw new Error(error);
    }

    return await response.text();
}