import {
    useEffect,
    useState
} from "react";

import {
    FaEdit,
    FaPlus,
    FaTrash
} from "react-icons/fa";

import Pagination from "../../components/common/Pagination";
import Toast from "../../components/common/Toast";

import usePagination from "../../hooks/usePagination";
import useToast from "../../hooks/useToast";

import {
    createQuiz,
    deleteQuiz,
    getCategories,
    getQuizzes,
    updateQuiz
} from "../../services/api";


const ITEMS_PER_PAGE = 5;

const EMPTY_FORM = {
    title: "",
    description: "",
    category_id: "",
    duration: "",
    total_marks: ""
};


const VALIDATION_RULES = {
    title: {
        label: "Quiz title",
        minLength: 3,
        maxLength: 100
    },
    description: {
        label: "Description",
        minLength: 5,
        maxLength: 255
    }
};


function QuizManagement() {

    const [
        quizzes,
        setQuizzes
    ] = useState([]);

    const [
        categories,
        setCategories
    ] = useState([]);

    const [
        formData,
        setFormData
    ] = useState(EMPTY_FORM);

    const [
        errors,
        setErrors
    ] = useState({});

    const [
        touched,
        setTouched
    ] = useState({});

    const [
        editingQuizId,
        setEditingQuizId
    ] = useState(null);

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        submitting,
        setSubmitting
    ] = useState(false);

    const [
        deletingQuizId,
        setDeletingQuizId
    ] = useState(null);


    const {
        toast,
        showSuccess,
        showError,
        clearToast
    } = useToast();


    const {
        currentPage,
        totalPages,
        paginatedItems: paginatedQuizzes,
        goToPreviousPage,
        goToNextPage
    } = usePagination(
        quizzes,
        ITEMS_PER_PAGE
    );


    const validateField = (
        name,
        value
    ) => {

        const stringValue = String(
            value ?? ""
        ).trim();


        if (
            name === "category_id"
        ) {

            return stringValue
                ? ""
                : "Category is required.";
        }


        if (
            name === "duration" ||
            name === "total_marks"
        ) {

            if (!stringValue) {

                return (
                    name === "duration"
                        ? "Duration is required."
                        : "Total marks is required."
                );
            }

            const numberValue = Number(
                stringValue
            );

            if (
                !Number.isInteger(
                    numberValue
                ) ||
                numberValue <= 0
            ) {

                return (
                    name === "duration"
                        ? (
                            "Duration must be a positive integer."
                        )
                        : (
                            "Total marks must be a positive integer."
                        )
                );
            }

            return "";
        }


        const rule = (
            VALIDATION_RULES[name]
        );

        if (!rule) {

            return "";
        }

        if (!stringValue) {

            return `${rule.label} is required.`;
        }

        if (
            stringValue.length <
            rule.minLength
        ) {

            return (
                `${rule.label} must be at least ` +
                `${rule.minLength} characters.`
            );
        }

        if (
            stringValue.length >
            rule.maxLength
        ) {

            return (
                `${rule.label} cannot exceed ` +
                `${rule.maxLength} characters.`
            );
        }

        return "";
    };


    const validateForm = () => {

        return Object.keys(
            EMPTY_FORM
        ).reduce(
            (
                validationErrors,
                fieldName
            ) => {

                validationErrors[
                    fieldName
                ] = validateField(
                    fieldName,
                    formData[fieldName]
                );

                return validationErrors;
            },
            {}
        );
    };


    const fetchData = async () => {

        setLoading(true);

        try {

            const [
                quizResponse,
                categoryResponse
            ] = await Promise.all([
                getQuizzes(),
                getCategories()
            ]);

            setQuizzes(
                Array.isArray(quizResponse)
                    ? quizResponse
                    : []
            );

            setCategories(
                Array.isArray(categoryResponse)
                    ? categoryResponse
                    : []
            );

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setLoading(false);
        }
    };


    useEffect(
        () => {

            fetchData();

        },
        []
    );


    const handleChange = (
        event
    ) => {

        const {
            name,
            value
        } = event.target;

        setFormData(
            previous => ({
                ...previous,
                [name]: value
            })
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
                [name]: validateField(
                    name,
                    value
                )
            })
        );
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
                    value
                )
            })
        );
    };


    const resetForm = () => {

        setFormData(
            EMPTY_FORM
        );

        setErrors({});

        setTouched({});

        setEditingQuizId(null);
    };


    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        const validationErrors = (
            validateForm()
        );

        setErrors(
            validationErrors
        );

        setTouched(
            Object.keys(
                EMPTY_FORM
            ).reduce(
                (
                    touchedFields,
                    fieldName
                ) => {

                    touchedFields[
                        fieldName
                    ] = true;

                    return touchedFields;
                },
                {}
            )
        );

        const hasErrors = Object.values(
            validationErrors
        ).some(Boolean);

        if (hasErrors) {

            return;
        }

        setSubmitting(true);

        const quizData = {
            title: formData.title.trim(),

            description: (
                formData.description.trim()
            ),

            category_id: (
                formData.category_id
            ),

            duration: Number(
                formData.duration
            ),

            total_marks: Number(
                formData.total_marks
            )
        };

        try {

            if (editingQuizId) {

                await updateQuiz(
                    editingQuizId,
                    quizData
                );

                showSuccess(
                    "Quiz updated successfully."
                );

            } else {

                await createQuiz(
                    quizData
                );

                showSuccess(
                    "Quiz created successfully."
                );
            }

            resetForm();

            await fetchData();

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setSubmitting(false);
        }
    };


    const handleEdit = (
        quiz
    ) => {

        setEditingQuizId(
            quiz.id
        );

        setFormData({
            title: quiz.title,
            description: quiz.description,
            category_id: quiz.category_id,
            duration: String(
                quiz.duration
            ),
            total_marks: String(
                quiz.total_marks
            )
        });

        setErrors({});

        setTouched({});

        clearToast();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    };


    const handleCancelEdit = () => {

        resetForm();

        clearToast();
    };


    const handleDelete = async (
        quiz
    ) => {

        const confirmed = window.confirm(
            `Are you sure you want to delete "${quiz.title}"?`
        );

        if (!confirmed) {

            return;
        }

        setDeletingQuizId(
            quiz.id
        );

        try {

            await deleteQuiz(
                quiz.id
            );

            if (
                editingQuizId === quiz.id
            ) {

                resetForm();
            }

            showSuccess(
                "Quiz deleted successfully."
            );

            await fetchData();

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setDeletingQuizId(null);
        }
    };


    const getCategoryName = (
        categoryId
    ) => {

        const category = categories.find(
            item => item.id === categoryId
        );

        return (
            category?.name ||
            "Unknown Category"
        );
    };


    const getInputClassName = (
        fieldName
    ) => {

        if (!touched[fieldName]) {

            return "form-input";
        }

        if (errors[fieldName]) {

            return "form-input input-error";
        }

        if (formData[fieldName]) {

            return "form-input input-valid";
        }

        return "form-input";
    };


    const isFormValid = () => {

        return Object.values(
            validateForm()
        ).every(
            error => !error
        );
    };


    return (

        <div className="quiz-management">

            <Toast
                toast={toast}
                onClose={clearToast}
            />


            <section className="management-form-card">

                <div className="section-heading">

                    <div>

                        <h2>
                            {
                                editingQuizId
                                    ? "Update Quiz"
                                    : "Create Quiz"
                            }
                        </h2>

                        <p>
                            {
                                editingQuizId
                                    ? (
                                        "Update the selected " +
                                        "quiz details."
                                    )
                                    : (
                                        "Create a new quiz " +
                                        "for a category."
                                    )
                            }
                        </p>

                    </div>

                </div>


                <form
                    onSubmit={handleSubmit}
                    noValidate
                >

                    <div className="form-group">

                        <label htmlFor="quiz-title">
                            Quiz Title
                        </label>

                        <input
                            id="quiz-title"
                            name="title"
                            type="text"
                            value={formData.title}
                            onChange={handleChange}
                            onBlur={handleBlur}
                            className={
                                getInputClassName(
                                    "title"
                                )
                            }
                            placeholder="Enter quiz title"
                            maxLength={100}
                        />

                        {
                            touched.title &&
                            errors.title && (

                                <p className="field-error">
                                    {errors.title}
                                </p>
                            )
                        }

                    </div>


                    <div className="form-group">

                        <label
                            htmlFor="quiz-description"
                        >
                            Description
                        </label>

                        <textarea
                            id="quiz-description"
                            name="description"
                            value={
                                formData.description
                            }
                            onChange={handleChange}
                            onBlur={handleBlur}
                            className={
                                getInputClassName(
                                    "description"
                                )
                            }
                            placeholder="Enter quiz description"
                            rows={4}
                            maxLength={255}
                        />

                        <div className="field-footer">

                            {
                                touched.description &&
                                errors.description ? (

                                    <p className="field-error">
                                        {
                                            errors.description
                                        }
                                    </p>

                                ) : (

                                    <span />

                                )
                            }

                            <span
                                className="character-count"
                            >
                                {
                                    formData
                                        .description
                                        .length
                                }/255
                            </span>

                        </div>

                    </div>


                    <div className="form-group">

                        <label
                            htmlFor="quiz-category"
                        >
                            Category
                        </label>

                        <select
                            id="quiz-category"
                            name="category_id"
                            value={
                                formData.category_id
                            }
                            onChange={handleChange}
                            onBlur={handleBlur}
                            className={
                                getInputClassName(
                                    "category_id"
                                )
                            }
                        >

                            <option value="">
                                Select a category
                            </option>

                            {
                                categories.map(
                                    category => (

                                        <option
                                            key={
                                                category.id
                                            }
                                            value={
                                                category.id
                                            }
                                        >
                                            {
                                                category.name
                                            }
                                        </option>
                                    )
                                )
                            }

                        </select>

                        {
                            touched.category_id &&
                            errors.category_id && (

                                <p className="field-error">
                                    {
                                        errors.category_id
                                    }
                                </p>
                            )
                        }

                    </div>


                    <div className="form-row">

                        <div className="form-group">

                            <label
                                htmlFor="quiz-duration"
                            >
                                Duration (minutes)
                            </label>

                            <input
                                id="quiz-duration"
                                name="duration"
                                type="number"
                                min="1"
                                step="1"
                                value={
                                    formData.duration
                                }
                                onChange={handleChange}
                                onBlur={handleBlur}
                                className={
                                    getInputClassName(
                                        "duration"
                                    )
                                }
                                placeholder="30"
                            />

                            {
                                touched.duration &&
                                errors.duration && (

                                    <p className="field-error">
                                        {
                                            errors.duration
                                        }
                                    </p>
                                )
                            }

                        </div>


                        <div className="form-group">

                            <label
                                htmlFor="quiz-total-marks"
                            >
                                Total Marks
                            </label>

                            <input
                                id="quiz-total-marks"
                                name="total_marks"
                                type="number"
                                min="1"
                                step="1"
                                value={
                                    formData.total_marks
                                }
                                onChange={handleChange}
                                onBlur={handleBlur}
                                className={
                                    getInputClassName(
                                        "total_marks"
                                    )
                                }
                                placeholder="100"
                            />

                            {
                                touched.total_marks &&
                                errors.total_marks && (

                                    <p className="field-error">
                                        {
                                            errors.total_marks
                                        }
                                    </p>
                                )
                            }

                        </div>

                    </div>


                    <div className="form-actions">

                        <button
                            type="submit"
                            className="primary-button"
                            disabled={
                                submitting ||
                                !isFormValid()
                            }
                        >

                            {
                                submitting ? (

                                    editingQuizId
                                        ? "Updating..."
                                        : "Creating..."

                                ) : (

                                    <>

                                        {
                                            editingQuizId
                                                ? <FaEdit />
                                                : <FaPlus />
                                        }

                                        <span>
                                            {
                                                editingQuizId
                                                    ? "Update Quiz"
                                                    : "Create Quiz"
                                            }
                                        </span>

                                    </>
                                )
                            }

                        </button>


                        {
                            editingQuizId && (

                                <button
                                    type="button"
                                    className="secondary-button"
                                    onClick={
                                        handleCancelEdit
                                    }
                                    disabled={submitting}
                                >
                                    Cancel
                                </button>
                            )
                        }

                    </div>

                </form>

            </section>


            <section className="management-list-card">

                <div className="section-heading">

                    <div>

                        <h2>
                            All Quizzes
                        </h2>

                        <p>
                            {quizzes.length} {
                                quizzes.length === 1
                                    ? "quiz"
                                    : "quizzes"
                            } available
                        </p>

                    </div>

                </div>


                {
                    loading ? (

                        <div className="loading-state">
                            Loading quizzes...
                        </div>

                    ) : quizzes.length === 0 ? (

                        <div className="empty-state">

                            <h3>
                                No quizzes found
                            </h3>

                            <p>
                                Create your first quiz
                                using the form above.
                            </p>

                        </div>

                    ) : (

                        <>

                            <div
                                className={
                                    "management-table-wrapper"
                                }
                            >

                                <table
                                    className="management-table"
                                >

                                    <thead>

                                        <tr>

                                            <th>
                                                Title
                                            </th>

                                            <th>
                                                Category
                                            </th>

                                            <th>
                                                Duration
                                            </th>

                                            <th>
                                                Marks
                                            </th>

                                            <th>
                                                Actions
                                            </th>

                                        </tr>

                                    </thead>


                                    <tbody>

                                        {
                                            paginatedQuizzes.map(
                                                quiz => (

                                                    <tr
                                                        key={
                                                            quiz.id
                                                        }
                                                    >

                                                        <td>

                                                            <strong>
                                                                {
                                                                    quiz.title
                                                                }
                                                            </strong>

                                                            <p
                                                                className={
                                                                    "table-description"
                                                                }
                                                            >
                                                                {
                                                                    quiz.description
                                                                }
                                                            </p>

                                                        </td>

                                                        <td>
                                                            {
                                                                getCategoryName(
                                                                    quiz.category_id
                                                                )
                                                            }
                                                        </td>

                                                        <td>
                                                            {
                                                                quiz.duration
                                                            } min
                                                        </td>

                                                        <td>
                                                            {
                                                                quiz.total_marks
                                                            }
                                                        </td>

                                                        <td>

                                                            <div
                                                                className={
                                                                    "table-actions"
                                                                }
                                                            >

                                                                <button
                                                                    type="button"
                                                                    className={
                                                                        "icon-button " +
                                                                        "edit-button"
                                                                    }
                                                                    onClick={
                                                                        () =>
                                                                            handleEdit(
                                                                                quiz
                                                                            )
                                                                    }
                                                                    aria-label={
                                                                        `Edit ${quiz.title}`
                                                                    }
                                                                >
                                                                    <FaEdit />
                                                                </button>


                                                                <button
                                                                    type="button"
                                                                    className={
                                                                        "icon-button " +
                                                                        "delete-button"
                                                                    }
                                                                    onClick={
                                                                        () =>
                                                                            handleDelete(
                                                                                quiz
                                                                            )
                                                                    }
                                                                    disabled={
                                                                        deletingQuizId ===
                                                                        quiz.id
                                                                    }
                                                                    aria-label={
                                                                        `Delete ${quiz.title}`
                                                                    }
                                                                >

                                                                    {
                                                                        deletingQuizId ===
                                                                        quiz.id
                                                                            ? "..."
                                                                            : <FaTrash />
                                                                    }

                                                                </button>

                                                            </div>

                                                        </td>

                                                    </tr>
                                                )
                                            )
                                        }

                                    </tbody>

                                </table>

                            </div>


                            <Pagination
                                currentPage={currentPage}
                                totalPages={totalPages}
                                onPrevious={
                                    goToPreviousPage
                                }
                                onNext={
                                    goToNextPage
                                }
                            />

                        </>

                    )
                }

            </section>

        </div>
    );
}


export default QuizManagement;