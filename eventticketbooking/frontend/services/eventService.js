const BASE_URL =
    "http://localhost:8082/api/v1/events";

// AUTH HEADERS
function getAuthHeaders() {

    const token =
        localStorage.getItem("token");

    return {

        "Authorization":
            `Bearer ${token}`
    };
}

// HANDLE ERROR RESPONSE
async function handleError(response) {
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

// GET ALL EVENTS
async function getAllEvents() {

    const response =
        await fetch(BASE_URL);

    if (!response.ok) {

        await handleError(response);
    }

    return await response.json();
}


// GET MY EVENTS

async function getMyEvents() {

    const response = await fetch(

        `${BASE_URL}/my-events`,

        {
            headers:
                getAuthHeaders()
        }
    );

    if (!response.ok) {

        await handleError(response);
    }

    return await response.json();
}


// GET EVENT BY ID
async function getEventById(id) {

    const response =
        await fetch(
            `${BASE_URL}/${id}`
        );

    if (!response.ok) {

        await handleError(response);
    }

    return await response.json();
}


// CREATE EVENT
async function createEvent(formData) {

    const response = await fetch(

        BASE_URL,

        {
            method: "POST",

            headers:
                getAuthHeaders(),

            body: formData
        }
    );

    if (!response.ok) {

        await handleError(response);
    }

    return await response.text();
}


// UPDATE EVENT
async function updateEvent(id, formData) {

    const response = await fetch(

        `${BASE_URL}/${id}`,

        {
            method: "PUT",

            headers:
                getAuthHeaders(),

            body: formData
        }
    );

    if (!response.ok) {

        await handleError(response);
    }

    return await response.text();
}

// DELETE EVENT

async function deleteEvent(id) {

    const response = await fetch(

        `${BASE_URL}/${id}`,

        {
            method: "DELETE",

            headers:
                getAuthHeaders()
        }
    );

    if (!response.ok) {

        await handleError(response);
    }

    return await response.text();
}