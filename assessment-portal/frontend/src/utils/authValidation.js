export const validateLoginField = (
    name,
    value
) => {

    switch (name) {

        case "username":

            if (!value.trim()) {

                return "Username is required.";
            }

            if (value.length < 3) {

                return (
                    "Username must be at least 3 characters."
                );
            }

            if (value.length > 30) {

                return (
                    "Username cannot exceed 30 characters."
                );
            }

            if (
                !/^[a-zA-Z0-9_]+$/.test(
                    value
                )
            ) {

                return (
                    "Username can contain only letters, numbers, and underscores."
                );
            }

            return "";


        case "password":

            if (!value) {

                return "Password is required.";
            }

            return "";


        default:

            return "";
    }
};


export const validateLoginForm = (
    data
) => {

    return {

        username: validateLoginField(
            "username",
            data.username
        ),

        password: validateLoginField(
            "password",
            data.password
        )
    };
};


export const validateRegisterField = (
    name,
    value,
    currentFormData
) => {

    switch (name) {

        case "username":

            if (!value.trim()) {

                return "Username is required.";
            }

            if (value.length < 3) {

                return (
                    "Username must be at least 3 characters."
                );
            }

            if (value.length > 30) {

                return (
                    "Username cannot exceed 30 characters."
                );
            }

            if (
                !/^[a-zA-Z0-9_]+$/.test(
                    value
                )
            ) {

                return (
                    "Username can contain only letters, numbers, and underscores."
                );
            }

            return "";


        case "email":

            if (!value.trim()) {

                return "Email is required.";
            }

            if (
                !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
                    value
                )
            ) {

                return (
                    "Enter a valid email address."
                );
            }

            return "";


        case "password":

            if (!value) {

                return "Password is required.";
            }

            if (value.length < 8) {

                return (
                    "Password must be at least 8 characters."
                );
            }

            if (value.length > 32) {

                return (
                    "Password cannot exceed 32 characters."
                );
            }

            if (
                !/[A-Z]/.test(
                    value
                )
            ) {

                return (
                    "Password must contain at least one uppercase letter."
                );
            }

            if (
                !/[a-z]/.test(
                    value
                )
            ) {

                return (
                    "Password must contain at least one lowercase letter."
                );
            }

            if (
                !/[0-9]/.test(
                    value
                )
            ) {

                return (
                    "Password must contain at least one number."
                );
            }

            if (
                !/[^A-Za-z0-9]/.test(
                    value
                )
            ) {

                return (
                    "Password must contain at least one special character."
                );
            }

            return "";


        case "confirmPassword":

            if (!value) {

                return (
                    "Please confirm your password."
                );
            }

            if (
                value !==
                currentFormData.password
            ) {

                return (
                    "Passwords do not match."
                );
            }

            return "";


        default:

            return "";
    }
};


export const validateRegisterForm = (
    data
) => {

    return {

        username: validateRegisterField(
            "username",
            data.username,
            data
        ),

        email: validateRegisterField(
            "email",
            data.email,
            data
        ),

        password: validateRegisterField(
            "password",
            data.password,
            data
        ),

        confirmPassword: validateRegisterField(
            "confirmPassword",
            data.confirmPassword,
            data
        )
    };
};