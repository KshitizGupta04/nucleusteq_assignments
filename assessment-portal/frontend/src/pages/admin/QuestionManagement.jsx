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
} from "../../services/adminService";


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
    options: [...MCQ_OPTIONS],
    correct_answer: "",
    question_type: "mcq",
    difficulty: "easy"
};


const getInitialOptions = (
    questionType
) => {

    if (
        questionType === "true_false"
    ) {

        return [
            ...TRUE_FALSE_OPTIONS
        ];
    }

    if (
        questionType === "short_answer"
    ) {

        return [];
    }

    return [
        ...MCQ_OPTIONS
    ];
};


const getQuestionTypeLabel = (
    questionType
) => {

    if (
        questionType === "true_false"
    ) {

        return "True / False";
    }

    if (
        questionType === "short_answer"
    ) {

        return "Short Answer";
    }

    if (
        questionType === "multiple_select"
    ) {

        return "Multiple Select";
    }

    return "MCQ";
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

    const [
        deletingQuestionId,
        setDeletingQuestionId
    ] = useState(null);

    const [
        questionToDelete,
        setQuestionToDelete
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

                question_type:
                    questionType,

                options:
                    getInitialOptions(
                        questionType
                    ),

                correct_answer:
                    questionType ===
                    "multiple_select"
                        ? []
                        : ""
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


                let updatedCorrectAnswer = (
                    previous.correct_answer
                );


                if (
                    previous.question_type ===
                    "multiple_select"
                ) {

                    const currentAnswers = (
                        Array.isArray(
                            previous.correct_answer
                        )
                            ? previous.correct_answer
                            : []
                    );

                    updatedCorrectAnswer = (
                        currentAnswers.map(
                            answer =>
                                answer === oldOption
                                    ? value
                                    : answer
                        )
                    );

                } else if (
                    previous.correct_answer ===
                    oldOption
                ) {

                    updatedCorrectAnswer = "";
                }


                return {
                    ...previous,

                    options:
                        updatedOptions,

                    correct_answer:
                        updatedCorrectAnswer
                };
            }
        );
    };


    const handleMultipleAnswerChange = (
        option
    ) => {

        setFormData(
            previous => {

                const currentAnswers = (
                    Array.isArray(
                        previous.correct_answer
                    )
                        ? previous.correct_answer
                        : []
                );


                const isSelected = (
                    currentAnswers.includes(
                        option
                    )
                );


                return {
                    ...previous,

                    correct_answer:
                        isSelected
                            ? currentAnswers.filter(
                                answer =>
                                    answer !== option
                            )
                            : [
                                ...currentAnswers,
                                option
                            ]
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


        if (
            formData.question.trim().length >
            500
        ) {

            showError(
                "Question cannot exceed 500 characters."
            );

            return false;
        }


        if (
            formData.question_type ===
            "short_answer"
        ) {

            if (
                !String(
                    formData.correct_answer
                ).trim()
            ) {

                showError(
                    "Correct answer is required."
                );

                return false;
            }

            return true;
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
                        "Question must contain " +
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
            formData.question_type ===
            "multiple_select"
        ) {

            const correctAnswers = (
                Array.isArray(
                    formData.correct_answer
                )
                    ? formData.correct_answer
                    : []
            );


            if (
                correctAnswers.length === 0
            ) {

                showError(
                    "Select at least one correct answer."
                );

                return false;
            }


            const hasInvalidAnswer = (
                correctAnswers.some(
                    answer =>
                        !cleanedOptions.includes(
                            answer.trim()
                        )
                )
            );


            if (hasInvalidAnswer) {

                showError(
                    "Every correct answer must be one of the options."
                );

                return false;
            }


            return true;
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


        if (!validateForm()) {

            return;
        }


        setSubmitting(true);


        try {

            const cleanedOptions = (
                formData.options.map(
                    option => option.trim()
                )
            );


            let correctAnswer = (
                formData.correct_answer
            );


            if (
                formData.question_type ===
                "short_answer"
            ) {

                correctAnswer = (
                    String(
                        formData.correct_answer
                    ).trim()
                );
            }


            if (
                formData.question_type ===
                "multiple_select"
            ) {

                correctAnswer = (
                    Array.isArray(
                        formData.correct_answer
                    )
                        ? formData.correct_answer.map(
                            answer =>
                                answer.trim()
                        )
                        : []
                );
            }


            const commonData = {
                question:
                    formData.question.trim(),

                options:
                    formData.question_type ===
                    "short_answer"
                        ? []
                        : cleanedOptions,

                correct_answer:
                    correctAnswer,

                question_type:
                    formData.question_type,

                difficulty:
                    formData.difficulty
            };


            let response;


            if (editingQuestionId) {

                response = await updateQuestion(
                    editingQuestionId,
                    commonData
                );

                showSuccess(
                    response?.message ||
                    "Question updated successfully."
                );

            } else {

                response = await createQuestion({
                    quiz_id: selectedQuizId,
                    ...commonData
                });

                showSuccess(
                    response?.message ||
                    "Question created successfully."
                );
            }


            resetForm();

            await loadQuestions(
                selectedQuizId
            );

        } catch (error) {

            showError(
                error.message ||
                "Failed to save question."
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


        let options = (
            getInitialOptions(
                questionType
            )
        );


        if (
            questionType !==
            "true_false" &&
            questionType !==
            "short_answer" &&
            Array.isArray(
                question.options
            )
        ) {

            options = [
                ...question.options
            ];
        }


        let correctAnswer = (
            question.correct_answer ?? ""
        );


        if (
            questionType ===
            "multiple_select"
        ) {

            correctAnswer = (
                Array.isArray(
                    question.correct_answer
                )
                    ? [
                        ...question.correct_answer
                    ]
                    : []
            );
        }


        setEditingQuestionId(
            question.id
        );


        setFormData({
            quiz_id:
                selectedQuizId,

            question:
                question.question || "",

            options,

            correct_answer:
                correctAnswer,

            question_type:
                questionType,

            difficulty:
                question.difficulty || "easy"
        });


        clearToast();


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    };


    const handleDeleteRequest = (
        question
    ) => {

        setQuestionToDelete(
            question
        );
    };


    const handleCancelDelete = () => {

        setQuestionToDelete(
            null
        );
    };


    const handleConfirmDelete = async () => {

        if (!questionToDelete) {

            return;
        }


        const question = (
            questionToDelete
        );


        setDeletingQuestionId(
            question.id
        );


        try {

            const response = (
                await deleteQuestion(
                    question.id
                )
            );


            if (
                editingQuestionId ===
                question.id
            ) {

                resetForm();
            }


            setQuestionToDelete(
                null
            );


            showSuccess(
                response?.message ||
                "Question deleted successfully."
            );


            await loadQuestions(
                selectedQuizId
            );

        } catch (error) {

            showError(
                error.message ||
                "Failed to delete question."
            );

        } finally {

            setDeletingQuestionId(
                null
            );
        }
    };


    const renderCorrectAnswer = (
        question
    ) => {

        if (
            Array.isArray(
                question.correct_answer
            )
        ) {

            return (
                question.correct_answer.join(
                    ", "
                )
            );
        }

        return (
            question.correct_answer || "-"
        );
    };


    return (

        <div className="question-management">

            <Toast
                toast={toast}
                onClose={clearToast}
            />


            {
                questionToDelete && (

                    <div className="confirmation-overlay">

                        <div className="confirmation-dialog">

                            <h3>
                                Delete Question
                            </h3>

                            <p>
                                Are you sure you want to delete
                                this question?
                            </p>

                            <div className="form-actions">

                                <button
                                    type="button"
                                    className="secondary-button"
                                    onClick={
                                        handleCancelDelete
                                    }
                                    disabled={
                                        deletingQuestionId !==
                                        null
                                    }
                                >
                                    Cancel
                                </button>

                                <button
                                    type="button"
                                    className="delete-button"
                                    onClick={
                                        handleConfirmDelete
                                    }
                                    disabled={
                                        deletingQuestionId !==
                                        null
                                    }
                                >

                                    {
                                        deletingQuestionId !==
                                        null
                                            ? "Deleting..."
                                            : "Delete"
                                    }

                                </button>

                            </div>

                        </div>

                    </div>
                )
            }


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
                            noValidate
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
                                    rows="4"
                                    required
                                />

                                <span
                                    className="character-count"
                                >
                                    {
                                        formData
                                            .question
                                            .length
                                    }/500
                                </span>

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

                                        <option value="short_answer">
                                            Short Answer
                                        </option>

                                        <option value="multiple_select">
                                            Multiple Select
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
                                "short_answer" ? (

                                    <div className="form-group">

                                        <label
                                            htmlFor="correct-answer-text"
                                        >
                                            Correct Answer
                                        </label>

                                        <input
                                            id="correct-answer-text"
                                            name="correct_answer"
                                            type="text"
                                            className="form-input"
                                            value={
                                                formData.correct_answer
                                            }
                                            onChange={
                                                handleInputChange
                                            }
                                            placeholder={
                                                "Enter the expected answer"
                                            }
                                            required
                                        />

                                    </div>

                                ) : (

                                    <>

                                        {
                                            formData.question_type ===
                                            "true_false" ? (

                                                <div className="form-group">

                                                    <label>
                                                        Options
                                                    </label>

                                                    <div
                                                        className={
                                                            "true-false-options"
                                                        }
                                                    >

                                                        <span
                                                            className={
                                                                "option-badge"
                                                            }
                                                        >
                                                            True
                                                        </span>

                                                        <span
                                                            className={
                                                                "option-badge"
                                                            }
                                                        >
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
                                                            className={
                                                                "form-group"
                                                            }
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
                                                                className={
                                                                    "form-input"
                                                                }
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


                                        {
                                            formData.question_type ===
                                            "multiple_select" ? (

                                                <div className="form-group">

                                                    <label>
                                                        Correct Answers
                                                    </label>

                                                    <div
                                                        className={
                                                            "multiple-select-options"
                                                        }
                                                    >

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

                                                                        <label
                                                                            key={
                                                                                `${option}-${index}`
                                                                            }
                                                                            className={
                                                                                "checkbox-option"
                                                                            }
                                                                        >

                                                                            <input
                                                                                type="checkbox"
                                                                                checked={
                                                                                    Array.isArray(
                                                                                        formData.correct_answer
                                                                                    ) &&
                                                                                    formData.correct_answer.includes(
                                                                                        option
                                                                                    )
                                                                                }
                                                                                onChange={
                                                                                    () =>
                                                                                        handleMultipleAnswerChange(
                                                                                            option
                                                                                        )
                                                                                }
                                                                            />

                                                                            <span>
                                                                                {
                                                                                    option
                                                                                }
                                                                            </span>

                                                                        </label>
                                                                    )
                                                                )
                                                        }

                                                    </div>

                                                </div>

                                            ) : (

                                                <div className="form-group">

                                                    <label
                                                        htmlFor="correct-answer"
                                                    >
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
                                                                            {
                                                                                option
                                                                            }
                                                                        </option>
                                                                    )
                                                                )
                                                        }

                                                    </select>

                                                </div>

                                            )
                                        }

                                    </>

                                )
                            }


                            <div className="form-actions">

                                <button
                                    type="submit"
                                    className="primary-button"
                                    disabled={submitting}
                                >

                                    {
                                        editingQuestionId
                                            ? <FaEdit />
                                            : <FaPlus />
                                    }

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
                                            disabled={submitting}
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
                            {
                                selectedQuizId
                                    ? (
                                        `${questions.length} ${
                                            questions.length === 1
                                                ? "question"
                                                : "questions"
                                        } available`
                                    )
                                    : (
                                        "View and manage questions " +
                                        "for the selected quiz."
                                    )
                            }
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
                                                                question.question
                                                            }
                                                        </td>

                                                        <td>
                                                            {
                                                                getQuestionTypeLabel(
                                                                    question
                                                                        .question_type
                                                                )
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
                                                                renderCorrectAnswer(
                                                                    question
                                                                )
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
                                                                                question
                                                                            )
                                                                    }
                                                                    aria-label={
                                                                        "Edit question"
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
                                                                            handleDeleteRequest(
                                                                                question
                                                                            )
                                                                    }
                                                                    disabled={
                                                                        deletingQuestionId ===
                                                                        question.id
                                                                    }
                                                                    aria-label={
                                                                        "Delete question"
                                                                    }
                                                                >

                                                                    {
                                                                        deletingQuestionId ===
                                                                        question.id
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