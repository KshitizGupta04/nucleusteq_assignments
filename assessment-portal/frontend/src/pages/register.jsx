import {
    useState
} from "react";

import {
    Link,
    useNavigate
} from "react-router-dom";

import {
    FaEye,
    FaEyeSlash
} from "react-icons/fa";

import {
    registerUser
} from "../services/api";


function Register() {

    const navigate = useNavigate();

    const [
        formData,
        setFormData
    ] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
    });

    const [
        errors,
        setErrors
    ] = useState({});

    const [
        touched,
        setTouched
    ] = useState({});

    const [
        serverError,
        setServerError
    ] = useState("");

    const [
        success,
        setSuccess
    ] = useState("");

    const [
        loading,
        setLoading
    ] = useState(false);

    const [
        showPassword,
        setShowPassword
    ] = useState(false);

    const [
        showConfirmPassword,
        setShowConfirmPassword
    ] = useState(false);


    const validateField = (
        name,
        value,
        currentFormData = formData
    ) => {

        switch (name) {

            case "username":

                if (!value.trim()) {

                    return "Username is required.";
                }

                if (value.length < 3) {

                    return "Username must be at least 3 characters.";
                }

                if (value.length > 30) {

                    return "Username cannot exceed 30 characters.";
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

                    return "Enter a valid email address.";
                }

                return "";


            case "password":

                if (!value) {

                    return "Password is required.";
                }

                if (value.length < 8) {

                    return "Password must be at least 8 characters.";
                }

                if (value.length > 32) {

                    return "Password cannot exceed 32 characters.";
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

                    return "Please confirm your password.";
                }

                if (
                    value !==
                    currentFormData.password
                ) {

                    return "Passwords do not match.";
                }

                return "";


            default:

                return "";
        }
    };


    const validateForm = (
        data
    ) => {

        return {
            username: validateField(
                "username",
                data.username,
                data
            ),

            email: validateField(
                "email",
                data.email,
                data
            ),

            password: validateField(
                "password",
                data.password,
                data
            ),

            confirmPassword: validateField(
                "confirmPassword",
                data.confirmPassword,
                data
            )
        };
    };


    const handleChange = (
        event
    ) => {

        const {
            name,
            value
        } = event.target;

        const updatedFormData = {
            ...formData,
            [name]: value
        };

        setFormData(
            updatedFormData
        );

        setTouched(
            previous => ({
                ...previous,
                [name]: true
            })
        );

        const updatedErrors = {
            ...errors,
            [name]: validateField(
                name,
                value,
                updatedFormData
            )
        };

        if (
            name === "password" &&
            touched.confirmPassword
        ) {

            updatedErrors.confirmPassword = (
                validateField(
                    "confirmPassword",
                    updatedFormData.confirmPassword,
                    updatedFormData
                )
            );
        }

        setErrors(
            updatedErrors
        );

        setServerError("");
    };


    const handleBlur = (
        event
    ) => {

        const {
            name,
            value
        } = event.target;

        setTouched(
            previous => ({
                ...previous,
                [name]: true
            })
        );

        setErrors(
            previous => ({
                ...previous,
                [name]: validateField(
                    name,
                    value,
                    formData
                )
            })
        );
    };


    const isFormValid = () => {

        const validationErrors = (
            validateForm(
                formData
            )
        );

        return Object.values(
            validationErrors
        ).every(
            error => !error
        );
    };


    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        setServerError("");

        setSuccess("");

        const validationErrors = (
            validateForm(
                formData
            )
        );

        setErrors(
            validationErrors
        );

        setTouched({
            username: true,
            email: true,
            password: true,
            confirmPassword: true
        });

        const hasErrors = Object.values(
            validationErrors
        ).some(
            error => error
        );

        if (hasErrors) {

            return;
        }

        setLoading(true);

        try {

            await registerUser(
                formData.username,
                formData.email,
                formData.password
            );

            setSuccess(
                "Registration successful. Redirecting to login..."
            );

            setTimeout(
                () => {

                    navigate(
                        "/login"
                    );

                },
                1500
            );

        } catch (error) {

            setServerError(
                error.message
            );

        } finally {

            setLoading(false);
        }
    };


    const getInputClassName = (
        fieldName
    ) => {

        if (
            touched[fieldName] &&
            errors[fieldName]
        ) {

            return "form-input input-error";
        }

        if (
            touched[fieldName] &&
            !errors[fieldName] &&
            formData[fieldName]
        ) {

            return "form-input input-valid";
        }

        return "form-input";
    };


    return (

        <div className="auth-page">

            <div className="auth-card">

                <div className="auth-header">

                    <h1>
                        Assessment Portal
                    </h1>

                    <p>
                        Create your candidate account
                    </p>

                </div>

                {
                    serverError && (

                        <div className="error-message">

                            {serverError}

                        </div>
                    )
                }

                {
                    success && (

                        <div className="success-message">

                            {success}

                        </div>
                    )
                }

                <form
                    onSubmit={
                        handleSubmit
                    }
                    noValidate
                >

                    <div className="form-group">

                        <label htmlFor="username">
                            Username
                        </label>

                        <input
                            id="username"
                            name="username"
                            type="text"
                            value={
                                formData.username
                            }
                            onChange={
                                handleChange
                            }
                            onBlur={
                                handleBlur
                            }
                            className={
                                getInputClassName(
                                    "username"
                                )
                            }
                            placeholder="Enter username"
                            autoComplete="username"
                        />

                        {
                            touched.username &&
                            errors.username && (

                                <p className="field-error">
                                    {errors.username}
                                </p>
                            )
                        }

                    </div>


                    <div className="form-group">

                        <label htmlFor="email">
                            Email
                        </label>

                        <input
                            id="email"
                            name="email"
                            type="email"
                            value={
                                formData.email
                            }
                            onChange={
                                handleChange
                            }
                            onBlur={
                                handleBlur
                            }
                            className={
                                getInputClassName(
                                    "email"
                                )
                            }
                            placeholder="Enter email"
                            autoComplete="email"
                        />

                        {
                            touched.email &&
                            errors.email && (

                                <p className="field-error">
                                    {errors.email}
                                </p>
                            )
                        }

                    </div>


                    <div className="form-group">

                        <label htmlFor="password">
                            Password
                        </label>

                        <div className="password-input-wrapper">

                            <input
                                id="password"
                                name="password"
                                type={
                                    showPassword
                                        ? "text"
                                        : "password"
                                }
                                value={
                                    formData.password
                                }
                                onChange={
                                    handleChange
                                }
                                onBlur={
                                    handleBlur
                                }
                                className={
                                    getInputClassName(
                                        "password"
                                    )
                                }
                                placeholder="Enter password"
                                autoComplete="new-password"
                            />

                            <button
                                type="button"
                                className="password-toggle"
                                onClick={
                                    () => setShowPassword(
                                        previous =>
                                            !previous
                                    )
                                }
                                aria-label={
                                    showPassword
                                        ? "Hide password"
                                        : "Show password"
                                }
                            >

                                {
                                    showPassword
                                        ? <FaEyeSlash />
                                        : <FaEye />
                                }

                            </button>

                        </div>

                        {
                            touched.password &&
                            errors.password && (

                                <p className="field-error">
                                    {errors.password}
                                </p>
                            )
                        }

                    </div>


                    <div className="form-group">

                        <label htmlFor="confirmPassword">
                            Confirm Password
                        </label>

                        <div className="password-input-wrapper">

                            <input
                                id="confirmPassword"
                                name="confirmPassword"
                                type={
                                    showConfirmPassword
                                        ? "text"
                                        : "password"
                                }
                                value={
                                    formData.confirmPassword
                                }
                                onChange={
                                    handleChange
                                }
                                onBlur={
                                    handleBlur
                                }
                                className={
                                    getInputClassName(
                                        "confirmPassword"
                                    )
                                }
                                placeholder="Confirm password"
                                autoComplete="new-password"
                            />

                            <button
                                type="button"
                                className="password-toggle"
                                onClick={
                                    () => setShowConfirmPassword(
                                        previous =>
                                            !previous
                                    )
                                }
                                aria-label={
                                    showConfirmPassword
                                        ? "Hide password"
                                        : "Show password"
                                }
                            >

                                {
                                    showConfirmPassword
                                        ? <FaEyeSlash />
                                        : <FaEye />
                                }

                            </button>

                        </div>

                        {
                            touched.confirmPassword &&
                            errors.confirmPassword && (

                                <p className="field-error">
                                    {errors.confirmPassword}
                                </p>
                            )
                        }

                    </div>


                    <button
                        className="primary-button"
                        type="submit"
                        disabled={
                            loading ||
                            !isFormValid()
                        }
                    >

                        {
                            loading
                                ? "Creating account..."
                                : "Register"
                        }

                    </button>

                </form>


                <div className="auth-footer">

                    <p>
                        Already have an account?{" "}

                        <Link to="/login">
                            Login
                        </Link>
                    </p>

                </div>

            </div>

        </div>
    );
}


export default Register;