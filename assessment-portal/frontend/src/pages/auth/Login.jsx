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
    loginUser
} from "../../services/authService";

import {
    validateLoginField,
    validateLoginForm
} from "../../utils/authValidation";


function Login() {

    const navigate = useNavigate();

    const [
        formData,
        setFormData
    ] = useState({
        username: "",
        password: ""
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
        loading,
        setLoading
    ] = useState(false);

    const [
        showPassword,
        setShowPassword
    ] = useState(false);


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

        setErrors(
            previous => ({
                ...previous,
                [name]: validateLoginField(
                    name,
                    value
                )
            })
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
                [name]: validateLoginField(
                    name,
                    value
                )
            })
        );
    };


    const isFormValid = () => {

        const validationErrors = (
            validateLoginForm(
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

        const validationErrors = (
            validateLoginForm(
                formData
            )
        );

        setErrors(
            validationErrors
        );

        setTouched({
            username: true,
            password: true
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

            const response = await loginUser(
                formData.username,
                formData.password
            );

            localStorage.setItem(
                "access_token",
                response.access_token
            );

            if (response.role) {

                localStorage.setItem(
                    "role",
                    response.role
                );
            }

            if (
                response.role === "admin"
            ) {

                navigate(
                    "/admin/dashboard"
                );

            } else {

                navigate(
                    "/student/dashboard"
                );
            }

        } catch {

            setServerError(
                "Invalid username or password."
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

            return (
                "form-input input-error"
            );
        }

        if (
            touched[fieldName] &&
            !errors[fieldName] &&
            formData[fieldName]
        ) {

            return (
                "form-input input-valid"
            );
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
                        Sign in to continue
                    </p>

                </div>


                {
                    serverError && (

                        <div className="error-message">

                            {serverError}

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

                        <label
                            htmlFor="username"
                        >
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

                                    {
                                        errors.username
                                    }

                                </p>
                            )
                        }

                    </div>


                    <div className="form-group">

                        <label
                            htmlFor="password"
                        >
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
                                autoComplete="current-password"
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

                                    {
                                        errors.password
                                    }

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
                                ? "Signing in..."
                                : "Login"
                        }

                    </button>

                </form>


                <div className="auth-footer">

                    <p>
                        New candidate?{" "}

                        <Link
                            to="/register"
                        >
                            Create an account
                        </Link>
                    </p>

                </div>

            </div>

        </div>
    );
}


export default Login;