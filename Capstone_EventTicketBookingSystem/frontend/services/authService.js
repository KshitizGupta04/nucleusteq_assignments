const AUTH_URL =
    "http://localhost:8081/auth";

// REGISTER USER
async function registerUser(userData) {

    try {

        const response = await fetch(

            `${AUTH_URL}/register`,

            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    userData
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

// LOGIN USER
async function loginUser(loginData) {

    try {

        const response = await fetch(

            `${AUTH_URL}/login`,

            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    loginData
                )
            }
        );

        const data =
            await response.json();

        if(!response.ok) {

            throw new Error(
                data.message ||
                "Login Failed"
            );
        }

        return data;

    } catch(error) {

        console.log(error);

        throw error;
    }
}

// LOGOUT
function logout() {

    localStorage.clear();

    window.location.href =
        "login.html";
}