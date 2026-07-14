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
} from "../../services/authService";

import {
    validateRegisterField,
    validateRegisterForm
} from "../../utils/authValidation";


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

            [name]: validateRegisterField(
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
                validateRegisterField(
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

                [name]: validateRegisterField(
                    name,
                    value,
                    formData
                )
            })
        );
    };


    const isFormValid = () => {

        const validationErrors = (
            validateRegisterForm(
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
            validateRegisterForm(
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
                "Registration successful. " +
                "Redirecting to login..."
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
                                    () =>
                                        setShowPassword(
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
                                    () =>
                                        setShowConfirmPassword(
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

                                    {
                                        errors.confirmPassword
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