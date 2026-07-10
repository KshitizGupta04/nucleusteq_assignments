import {
    encryptPassword
} from "../utils/passwordEncryption";


const API_BASE_URL = (
    "http://127.0.0.1:8000/api/v1"
);


export const apiRequest = async (
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
                    (error) => error.msg
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

export const loginUser = async (
    username,
    password
) => {

    const encryptedPassword = (
        await encryptPassword(
            password
        )
    );

    return apiRequest(
        "/auth/login",
        {
            method: "POST",

            body: JSON.stringify({
                username,
                password: encryptedPassword
            })
        }
    );
};


export const registerUser = async (
    username,
    email,
    password
) => {

    const encryptedPassword = (
        await encryptPassword(
            password
        )
    );

    return apiRequest(
        "/auth/register",
        {
            method: "POST",

            body: JSON.stringify({
                username,
                email,
                password: encryptedPassword
            })
        }
    );
};