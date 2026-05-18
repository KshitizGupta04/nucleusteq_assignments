const EVENT_URL =
    "http://localhost:8082/events";

// GET TOKEN
function getToken() {

    return localStorage.getItem(
        "token"
    );
}

// GET HEADERS
function getAuthHeaders() {

    return {

        "Content-Type":
            "application/json",

        Authorization:
            `Bearer ${getToken()}`
    };
}

// GET ALL EVENTS
async function getAllEvents() {

    try {

        const response =
            await fetch(EVENT_URL);

        if(!response.ok) {

            throw new Error(
                "Failed to fetch events"
            );
        }

        return await response.json();

    } catch(error) {

        console.log(error);

        throw error;
    }
}

// GET EVENT BY ID
async function getEventById(id) {

    try {

        const response = await fetch(

            `${EVENT_URL}/${id}`
        );

        if(!response.ok) {

            throw new Error(
                "Event not found"
            );
        }

        return await response.json();

    } catch(error) {

        console.log(error);

        throw error;
    }
}

// CREATE EVENT
async function createEvent(eventData) {

    try {

        const response = await fetch(

            EVENT_URL,

            {
                method: "POST",

                headers:
                    getAuthHeaders(),

                body: JSON.stringify(
                    eventData
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

// UPDATE EVENT
async function updateEvent(
    id,
    eventData
) {

    try {

        const response = await fetch(

            `${EVENT_URL}/${id}`,

            {
                method: "PUT",

                headers:
                    getAuthHeaders(),

                body: JSON.stringify(
                    eventData
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

// DELETE EVENT
async function deleteEvent(id) {

    try {

        const response = await fetch(

            `${EVENT_URL}/${id}`,

            {
                method: "DELETE",

                headers:
                    getAuthHeaders()
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