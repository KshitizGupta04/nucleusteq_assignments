document.documentElement.setAttribute(
    "data-theme",
    localStorage.getItem("theme") || "dark"
);

// SESSION EXPIRED MESSAGE

const sessionExpired =

    localStorage.getItem(
        "sessionExpired"
    );

if (sessionExpired === "true") {

    showToast(

        "Session expired. Please login again.",

        "error"
    );

    localStorage.removeItem(
        "sessionExpired"
    );
}



// SHOW / HIDE PASSWORD


function togglePassword() {

    const passwordInput =
        document.getElementById(
            "password"
        );

    passwordInput.type =

        passwordInput.type === "password"

            ? "text"

            : "password";
}



// LOGIN FORM
document.getElementById("loginForm")
    .addEventListener("submit", async function (e) {

        e.preventDefault();

        const email =
            document.getElementById(
                "email"
            ).value.trim();

        const password =
            document.getElementById(
                "password"
            ).value.trim();

        clearErrors(

            "emailError",

            "passwordError",

            "loginError"
        );

        let isValid = true;



        // EMAIL VALIDATION


        if (email === "") {

            setError(

                "emailError",

                "Email is required"
            );

            isValid = false;

        } else if (!validateEmail(email)) {

            setError(

                "emailError",

                "Invalid email format"
            );

            isValid = false;
        }



        // PASSWORD VALIDATION


        if (password === "") {

            setError(

                "passwordError",

                "Password is required"
            );

            isValid = false;

        } else if (password.length < 6) {

            setError(

                "passwordError",

                "Password must be at least 6 characters"
            );

            isValid = false;
        }

        if (!isValid) return;



        // LOGIN API


        try {

            const response =
                await loginUser({

                    email,

                    password
                });



            // DECODE JWT

            const payload = JSON.parse(

                atob(
                    response.token
                        .split(".")[1]
                )
            );



            // SAVE LOGIN DATA


            localStorage.setItem(

                "token",

                response.token
            );

            localStorage.setItem(

                "role",

                payload.role
            );



            // SUCCESS TOAST


            showToast(

                "Login successful!",

                "success"
            );


            // REDIRECT

            setTimeout(() => {

                window.location.href =

                    payload.role === "ORGANISER"

                        ? "dashboard.html"

                        : "home.html";

            }, 800);

        } catch (error) {

            let message =
                error.message;

            try {

                const parsed =
                    JSON.parse(message);

                message =

                    parsed.message

                    ||

                    "Login failed";

            } catch (_) {

                // already plain string
            }

            setError(
                "loginError",
                message
            );
        }
    });