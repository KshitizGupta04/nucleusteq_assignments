const BOOKING_URL =
    "http://localhost:8082/bookings";

// GET TOKEN
function getBookingToken() {

    return localStorage.getItem(
        "token"
    );
}

// AUTH HEADERS
function getBookingHeaders() {

    return {

        "Content-Type":
            "application/json",

        Authorization:
            `Bearer ${getBookingToken()}`
    };
}

// BOOK TICKETS
async function bookTickets(bookingData) {

    try {

        const response = await fetch(

            BOOKING_URL,

            {
                method: "POST",

                headers:
                    getBookingHeaders(),

                body: JSON.stringify(
                    bookingData
                )
            }
        );

        const data =
            await response.text();

        if(!response.ok) {

            throw new Error(data);
        }

        return data;

    } catch(error) {

        console.log(error);

        throw error;
    }
}

// GET MY BOOKINGS
async function getMyBookings() {

    try {

        const response = await fetch(

            `${BOOKING_URL}/my-bookings`,

            {
                headers:
                    getBookingHeaders()
            }
        );

        if(!response.ok) {

            throw new Error(
                "Failed to fetch bookings"
            );
        }

        return await response.json();

    } catch(error) {

        console.log(error);

        throw error;
    }
}

// CANCEL BOOKING
async function cancelBooking(id) {

    try {

        const response = await fetch(

            `${BOOKING_URL}/${id}`,

            {
                method: "DELETE",

                headers:
                    getBookingHeaders()
            }
        );

        const data =
            await response.text();

        if(!response.ok) {

            throw new Error(data);
        }

        return data;

    } catch(error) {

        console.log(error);

        throw error;
    }
}