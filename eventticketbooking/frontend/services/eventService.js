const EVENT_URL = "http://localhost:8082/api/v1/events";

function getToken() {
    return localStorage.getItem("token");
}

function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`
    };
}

async function getAllEvents() {
    const response = await fetch(EVENT_URL);
    if (!response.ok) throw new Error("Failed to fetch events");
    return await response.json();
}

async function getEventById(id) {
    const response = await fetch(`${EVENT_URL}/${id}`);
    if (!response.ok) throw new Error("Event not found");
    return await response.json();
}

async function createEvent(eventData) {
    const response = await fetch(EVENT_URL, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(eventData)
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error);
    }

    return await response.text();
}

async function updateEvent(id, eventData) {
    const response = await fetch(`${EVENT_URL}/${id}`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify(eventData)
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error);
    }

    return await response.text();
}

async function deleteEvent(id) {
    const response = await fetch(`${EVENT_URL}/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${getToken()}` }
    });

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error);
    }

    return await response.text();
}
