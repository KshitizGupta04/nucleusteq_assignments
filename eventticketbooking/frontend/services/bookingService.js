const BOOKING_URL = "http://localhost:8082/api/v1/bookings";

function getToken() {
    return localStorage.getItem("token");
}

async function bookTickets(bookingData) {
    const response = await fetch(BOOKING_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify(bookingData)
    });

    const data = await response.text();
    if (!response.ok) throw new Error(data);
    return data;
}

async function getMyBookings() {
    const response = await fetch(`${BOOKING_URL}/my-bookings`, {
        headers: { "Authorization": `Bearer ${getToken()}` }
    });

    if (!response.ok) throw new Error("Failed to fetch bookings");
    return await response.json();
}

async function cancelBooking(id) {
    const response = await fetch(`${BOOKING_URL}/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${getToken()}` }
    });

    const data = await response.text();
    if (!response.ok) throw new Error(data);
    return data;
}
