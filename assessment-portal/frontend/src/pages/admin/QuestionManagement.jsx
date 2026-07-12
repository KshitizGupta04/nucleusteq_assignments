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
    createQuestion,
    deleteQuestion,
    getAdminQuestionsByQuiz,
    getQuizzes,
    updateQuestion
} from "../../services/api";


const ITEMS_PER_PAGE = 5;

const MCQ_OPTIONS = [
    "",
    "",
    "",
    ""
];

const TRUE_FALSE_OPTIONS = [
    "True",
    "False"
];


const INITIAL_FORM = {
    quiz_id: "",
    question: "",
    options: MCQ_OPTIONS,
    correct_answer: "",
    question_type: "mcq",
    difficulty: "easy"
};


function QuestionManagement() {

    const [
        quizzes,
        setQuizzes
    ] = useState([]);

    const [
        questions,
        setQuestions
    ] = useState([]);

    const [
        selectedQuizId,
        setSelectedQuizId
    ] = useState("");

    const [
        formData,
        setFormData
    ] = useState({
        ...INITIAL_FORM,
        options: [...MCQ_OPTIONS]
    });

    const [
        editingQuestionId,
        setEditingQuestionId
    ] = useState(null);

    const [
        loading,
        setLoading
    ] = useState(false);

    const [
        submitting,
        setSubmitting
    ] = useState(false);


    const {
        toast,
        showSuccess,
        showError,
        clearToast
    } = useToast();


    const {
        currentPage,
        totalPages,
        paginatedItems: paginatedQuestions,
        goToPreviousPage,
        goToNextPage,
        resetPage
    } = usePagination(
        questions,
        ITEMS_PER_PAGE
    );


    const loadQuizzes = async () => {

        try {

            const response = await getQuizzes();

            setQuizzes(
                Array.isArray(response)
                    ? response
                    : []
            );

        } catch (error) {

            showError(
                error.message
            );
        }
    };


    const loadQuestions = async (
        quizId
    ) => {

        if (!quizId) {

            setQuestions([]);

            return;
        }

        setLoading(true);

        try {

            const response = (
                await getAdminQuestionsByQuiz(
                    quizId
                )
            );

            setQuestions(
                Array.isArray(response)
                    ? response
                    : []
            );

            resetPage();

        } catch (error) {

            setQuestions([]);

            showError(
                error.message
            );

        } finally {

            setLoading(false);
        }
    };


    useEffect(
        () => {

            loadQuizzes();

        },
        []
    );


    const resetForm = () => {

        setFormData({
            ...INITIAL_FORM,
            quiz_id: selectedQuizId,
            options: [...MCQ_OPTIONS]
        });

        setEditingQuestionId(null);
    };


    const handleQuizChange = (
        event
    ) => {

        const quizId = (
            event.target.value
        );

        setSelectedQuizId(
            quizId
        );

        setFormData({
            ...INITIAL_FORM,
            quiz_id: quizId,
            options: [...MCQ_OPTIONS]
        });

        setEditingQuestionId(null);

        loadQuestions(
            quizId
        );
    };


    const handleInputChange = (
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
    };


    const handleQuestionTypeChange = (
        event
    ) => {

        const questionType = (
            event.target.value
        );

        setFormData(
            previous => ({
                ...previous,

                question_type: questionType,

                options:
                    questionType === "true_false"
                        ? [...TRUE_FALSE_OPTIONS]
                        : [...MCQ_OPTIONS],

                correct_answer: ""
            })
        );
    };


    const handleOptionChange = (
        index,
        value
    ) => {

        setFormData(
            previous => {

                const updatedOptions = [
                    ...previous.options
                ];

                const oldOption = (
                    updatedOptions[index]
                );

                updatedOptions[index] = value;

                return {
                    ...previous,

                    options: updatedOptions,

                    correct_answer:
                        previous.correct_answer ===
                        oldOption
                            ? ""
                            : previous.correct_answer
                };
            }
        );
    };


    const validateForm = () => {

        if (!selectedQuizId) {

            showError(
                "Please select a quiz."
            );

            return false;
        }


        if (
            formData.question.trim().length <
            5
        ) {

            showError(
                "Question must contain at least 5 characters."
            );

            return false;
        }


        const expectedOptionCount = (
            formData.question_type ===
            "true_false"
                ? 2
                : 4
        );


        if (
            formData.options.length !==
            expectedOptionCount
        ) {

            showError(
                formData.question_type ===
                "true_false"
                    ? (
                        "True/False question must " +
                        "contain exactly 2 options."
                    )
                    : (
                        "MCQ question must contain " +
                        "exactly 4 options."
                    )
            );

            return false;
        }


        const cleanedOptions = (
            formData.options.map(
                option => option.trim()
            )
        );


        if (
            cleanedOptions.some(
                option => !option
            )
        ) {

            showError(
                "All options are required."
            );

            return false;
        }


        if (
            new Set(
                cleanedOptions
            ).size !==
            cleanedOptions.length
        ) {

            showError(
                "All options must be unique."
            );

            return false;
        }


        if (
            !formData.correct_answer
        ) {

            showError(
                "Please select the correct answer."
            );

            return false;
        }


        if (
            !cleanedOptions.includes(
                formData.correct_answer
            )
        ) {

            showError(
                "Correct answer must be one of the options."
            );

            return false;
        }


        return true;
    };


    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        console.log(
        "CREATE QUESTION SUBMIT CLICKED",
        formData,
        selectedQuizId
        );


        const isValid = validateForm();

        console.log(
            "VALIDATION RESULT:",
            isValid
        );

        if (!isValid) {

            return;
        }

        console.log(
            "VALIDATION PASSED - CALLING API"
        );

        setSubmitting(true);

        try {

            const cleanedOptions = (
                formData.options.map(
                    option => option.trim()
                )
            );


            const commonData = {
                question:
                    formData.question.trim(),

                options: cleanedOptions,

                correct_answer:
                    formData.correct_answer,

                question_type:
                    formData.question_type,

                difficulty:
                    formData.difficulty
            };


            if (editingQuestionId) {

                await updateQuestion(
                    editingQuestionId,
                    commonData
                );

                showSuccess(
                    "Question updated successfully."
                );

            } else {

                await createQuestion({
                    quiz_id: selectedQuizId,
                    ...commonData
                });

                showSuccess(
                    "Question created successfully."
                );
            }


            resetForm();

            await loadQuestions(
                selectedQuizId
            );

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setSubmitting(false);
        }
    };


    const handleEdit = (
        question
    ) => {

        const questionType = (
            question.question_type ||
            "mcq"
        );

        const options = (
            questionType === "true_false"
                ? [...TRUE_FALSE_OPTIONS]
                : (
                    Array.isArray(
                        question.options
                    )
                        ? [...question.options]
                        : [...MCQ_OPTIONS]
                )
        );


        setEditingQuestionId(
            question.id
        );

        setFormData({
            quiz_id: selectedQuizId,

            question:
                question.question || "",

            options,

            correct_answer:
                question.correct_answer || "",

            question_type:
                questionType,

            difficulty:
                question.difficulty || "easy"
        });


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    };


    const handleDelete = async (
        questionId
    ) => {

        const confirmed = window.confirm(
            "Are you sure you want to delete this question?"
        );

        if (!confirmed) {

            return;
        }

        try {

            await deleteQuestion(
                questionId
            );

            showSuccess(
                "Question deleted successfully."
            );

            await loadQuestions(
                selectedQuizId
            );

        } catch (error) {

            showError(
                error.message
            );
        }
    };


    return (

        <div className="question-management">

            <Toast
                toast={toast}
                onClose={clearToast}
            />


            <div className="management-form-card">

                <div className="section-heading">

                    <div>

                        <h2>
                            {
                                editingQuestionId
                                    ? "Edit Question"
                                    : "Create Question"
                            }
                        </h2>

                        <p>
                            Select a quiz and manage
                            its assessment questions.
                        </p>

                    </div>

                </div>


                <div className="form-group">

                    <label htmlFor="question-quiz">
                        Select Quiz
                    </label>

                    <select
                        id="question-quiz"
                        className="form-input"
                        value={selectedQuizId}
                        onChange={handleQuizChange}
                    >

                        <option value="">
                            Select a quiz
                        </option>

                        {
                            quizzes.map(
                                quiz => (

                                    <option
                                        key={quiz.id}
                                        value={quiz.id}
                                    >
                                        {quiz.title}
                                    </option>
                                )
                            )
                        }

                    </select>

                </div>


                {
                    selectedQuizId && (

                        <form
                            onSubmit={handleSubmit}
                        >

                            <div className="form-group">

                                <label htmlFor="question">
                                    Question
                                </label>

                                <textarea
                                    id="question"
                                    name="question"
                                    className="form-input"
                                    value={
                                        formData.question
                                    }
                                    onChange={
                                        handleInputChange
                                    }
                                    minLength="5"
                                    maxLength="500"
                                    required
                                />

                            </div>


                            <div className="form-row">

                                <div className="form-group">

                                    <label
                                        htmlFor="question-type"
                                    >
                                        Question Type
                                    </label>

                                    <select
                                        id="question-type"
                                        name="question_type"
                                        className="form-input"
                                        value={
                                            formData.question_type
                                        }
                                        onChange={
                                            handleQuestionTypeChange
                                        }
                                    >

                                        <option value="mcq">
                                            MCQ
                                        </option>

                                        <option value="true_false">
                                            True / False
                                        </option>

                                    </select>

                                </div>


                                <div className="form-group">

                                    <label htmlFor="difficulty">
                                        Difficulty
                                    </label>

                                    <select
                                        id="difficulty"
                                        name="difficulty"
                                        className="form-input"
                                        value={
                                            formData.difficulty
                                        }
                                        onChange={
                                            handleInputChange
                                        }
                                    >

                                        <option value="easy">
                                            Easy
                                        </option>

                                        <option value="medium">
                                            Medium
                                        </option>

                                        <option value="hard">
                                            Hard
                                        </option>

                                    </select>

                                </div>

                            </div>


                            {
                                formData.question_type ===
                                "true_false" ? (

                                    <div className="form-group">

                                        <label>
                                            Options
                                        </label>

                                        <div className="true-false-options">

                                            <span className="option-badge">
                                                True
                                            </span>

                                            <span className="option-badge">
                                                False
                                            </span>

                                        </div>

                                    </div>

                                ) : (

                                    formData.options.map(
                                        (
                                            option,
                                            index
                                        ) => (

                                            <div
                                                className="form-group"
                                                key={index}
                                            >

                                                <label
                                                    htmlFor={
                                                        `option-${index}`
                                                    }
                                                >
                                                    Option {
                                                        index + 1
                                                    }
                                                </label>

                                                <input
                                                    id={
                                                        `option-${index}`
                                                    }
                                                    type="text"
                                                    className="form-input"
                                                    value={option}
                                                    onChange={
                                                        event =>
                                                            handleOptionChange(
                                                                index,
                                                                event
                                                                    .target
                                                                    .value
                                                            )
                                                    }
                                                    required
                                                />

                                            </div>
                                        )
                                    )

                                )
                            }


                            <div className="form-group">

                                <label htmlFor="correct-answer">
                                    Correct Answer
                                </label>

                                <select
                                    id="correct-answer"
                                    name="correct_answer"
                                    className="form-input"
                                    value={
                                        formData.correct_answer
                                    }
                                    onChange={
                                        handleInputChange
                                    }
                                    required
                                >

                                    <option value="">
                                        Select correct answer
                                    </option>

                                    {
                                        formData.options
                                            .filter(
                                                option =>
                                                    option.trim()
                                            )
                                            .map(
                                                (
                                                    option,
                                                    index
                                                ) => (

                                                    <option
                                                        key={
                                                            `${option}-${index}`
                                                        }
                                                        value={option}
                                                    >
                                                        {option}
                                                    </option>
                                                )
                                            )
                                    }

                                </select>

                            </div>


                            <div className="form-actions">

                                <button
                                    type="submit"
                                    className="primary-button"
                                    disabled={submitting}
                                >

                                    <FaPlus />

                                    {
                                        submitting
                                            ? "Saving..."
                                            : editingQuestionId
                                                ? "Update Question"
                                                : "Create Question"
                                    }

                                </button>


                                {
                                    editingQuestionId && (

                                        <button
                                            type="button"
                                            className="secondary-button"
                                            onClick={resetForm}
                                        >
                                            Cancel
                                        </button>

                                    )
                                }

                            </div>

                        </form>

                    )
                }

            </div>


            <div className="management-list-card">

                <div className="section-heading">

                    <div>

                        <h2>
                            Questions
                        </h2>

                        <p>
                            View and manage questions
                            for the selected quiz.
                        </p>

                    </div>

                </div>


                {
                    !selectedQuizId ? (

                        <div className="empty-state">

                            <h3>
                                Select a quiz
                            </h3>

                            <p>
                                Choose a quiz to view
                                its questions.
                            </p>

                        </div>

                    ) : loading ? (

                        <div className="loading-state">
                            Loading questions...
                        </div>

                    ) : questions.length === 0 ? (

                        <div className="empty-state">

                            <h3>
                                No questions found
                            </h3>

                            <p>
                                Create the first question
                                for this quiz.
                            </p>

                        </div>

                    ) : (

                        <>

                            <div className="management-table-wrapper">

                                <table className="management-table">

                                    <thead>

                                        <tr>

                                            <th>
                                                Question
                                            </th>

                                            <th>
                                                Type
                                            </th>

                                            <th>
                                                Difficulty
                                            </th>

                                            <th>
                                                Correct Answer
                                            </th>

                                            <th>
                                                Actions
                                            </th>

                                        </tr>

                                    </thead>


                                    <tbody>

                                        {
                                            paginatedQuestions.map(
                                                question => (

                                                    <tr
                                                        key={
                                                            question.id
                                                        }
                                                    >

                                                        <td>
                                                            {
                                                                question
                                                                    .question
                                                            }
                                                        </td>

                                                        <td>
                                                            {
                                                                question
                                                                    .question_type ===
                                                                "true_false"
                                                                    ? "True / False"
                                                                    : "MCQ"
                                                            }
                                                        </td>

                                                        <td>
                                                            {
                                                                question
                                                                    .difficulty
                                                            }
                                                        </td>

                                                        <td>
                                                            {
                                                                question
                                                                    .correct_answer
                                                            }
                                                        </td>

                                                        <td>

                                                            <div className="table-actions">

                                                                <button
                                                                    type="button"
                                                                    className={
                                                                        "icon-button " +
                                                                        "edit-button"
                                                                    }
                                                                    onClick={
                                                                        () =>
                                                                            handleEdit(
                                                                                question
                                                                            )
                                                                    }
                                                                    aria-label="Edit question"
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
                                                                                question.id
                                                                            )
                                                                    }
                                                                    aria-label="Delete question"
                                                                >
                                                                    <FaTrash />
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
                                currentPage={
                                    currentPage
                                }
                                totalPages={
                                    totalPages
                                }
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

            </div>

        </div>
    );
}


export default QuestionManagement;