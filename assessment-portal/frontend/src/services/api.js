const API_BASE_URL = (
    "http://127.0.0.1:8000/api/v1"
);


const apiRequest = async (
    endpoint,
    options = {}
) => {

    const token = localStorage.getItem(
        "access_token"
    );

    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };


    if (token) {

        headers.Authorization = (
            `Bearer ${token}`
        );
    }


    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers
        }
    );


    let data;


    try {

        data = await response.json();

    } catch {

        data = {};
    }


    if (!response.ok) {

        let errorMessage = (
            "Something went wrong."
        );


        if (
            typeof data.detail === "string"
        ) {

            errorMessage = data.detail;

        } else if (
            Array.isArray(data.detail)
        ) {

            errorMessage = data.detail
                .map(
                    error => error.msg
                )
                .join(", ");

        } else if (
            data.detail &&
            typeof data.detail === "object"
        ) {

            errorMessage = (
                data.detail.message ||
                JSON.stringify(
                    data.detail
                )
            );
        }


        throw new Error(
            errorMessage
        );
    }


    return data;
};


export const get = async (
    endpoint
) => {

    return apiRequest(
        endpoint,
        {
            method: "GET"
        }
    );
};


export const post = async (
    endpoint,
    body
) => {

    return apiRequest(
        endpoint,
        {
            method: "POST",

            body: JSON.stringify(
                body
            )
        }
    );
};


export const put = async (
    endpoint,
    body
) => {

    return apiRequest(
        endpoint,
        {
            method: "PUT",

            body: JSON.stringify(
                body
            )
        }
    );
};


export const deleteRequest = async (
    endpoint
) => {

    return apiRequest(
        endpoint,
        {
            method: "DELETE"
        }
    );
};


export const getRequest = get;

export const postRequest = post;

export const putRequest = put;

export const del = deleteRequest;