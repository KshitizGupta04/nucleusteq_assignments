import {
    useCallback,
    useEffect,
    useRef,
    useState
} from "react";

import {
    FaArrowLeft,
    FaArrowRight,
    FaClipboardCheck,
    FaClock
} from "react-icons/fa";

import {
    resumeAttempt,
    saveAttemptAnswer,
    submitAttempt
} from "../../services/studentService";


function QuizAttempt({
    attemptId,
    onSubmitted
}) {

    const [
        attempt,
        setAttempt
    ] = useState(null);

    const [
        answers,
        setAnswers
    ] = useState({});

    const [
        currentQuestionIndex,
        setCurrentQuestionIndex
    ] = useState(0);

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        error,
        setError
    ] = useState("");

    const [
        savingQuestionId,
        setSavingQuestionId
    ] = useState(null);

    const [
        submitting,
        setSubmitting
    ] = useState(false);

    const [
        remainingSeconds,
        setRemainingSeconds
    ] = useState(null);


    const answersRef = useRef({});

    const autoSubmittingRef = useRef(false);

    const submissionCompletedRef = useRef(false);

    const shortAnswerTimersRef = useRef({});


    useEffect(
        () => {

            answersRef.current = answers;

        },
        [
            answers
        ]
    );


    useEffect(
        () => {

            const timers = (
                shortAnswerTimersRef.current
            );


            return () => {

                Object.values(
                    timers
                ).forEach(
                    timerId => {

                        clearTimeout(
                            timerId
                        );
                    }
                );
            };

        },
        []
    );


    useEffect(
        () => {

            const loadAttempt = async () => {

                if (!attemptId) {

                    setError(
                        "Attempt ID is missing."
                    );

                    setLoading(false);

                    return;
                }


                try {

                    setLoading(true);

                    setError("");


                    const data = (
                        await resumeAttempt(
                            attemptId
                        )
                    );


                    if (
                        data.status ===
                        "submitted"
                    ) {

                        submissionCompletedRef.current = (
                            true
                        );

                        onSubmitted();

                        return;
                    }


                    setAttempt(
                        data
                    );


                    const savedAnswers = (
                        data.answers || {}
                    );


                    setAnswers(
                        savedAnswers
                    );

                    answersRef.current = (
                        savedAnswers
                    );


                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load attempt."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadAttempt();

        },
        [
            attemptId,
            onSubmitted
        ]
    );


    const submitQuiz = useCallback(
        async (
            isAutoSubmit = false
        ) => {

            if (
                submissionCompletedRef.current ||
                autoSubmittingRef.current
            ) {

                return;
            }


            autoSubmittingRef.current = true;


            try {

                setSubmitting(true);

                setError("");


                await submitAttempt(
                    attemptId,
                    answersRef.current
                );


                submissionCompletedRef.current = (
                    true
                );


                onSubmitted();


            } catch (err) {

                const message = (
                    err.message ||
                    "Failed to submit attempt."
                );


                if (
                    message
                        .toLowerCase()
                        .includes(
                            "already submitted"
                        )
                ) {

                    submissionCompletedRef.current = (
                        true
                    );

                    onSubmitted();

                    return;
                }


                setError(
                    isAutoSubmit
                        ? (
                            "Quiz could not be " +
                            "automatically submitted. " +
                            message
                        )
                        : message
                );


            } finally {

                setSubmitting(false);


                if (
                    !submissionCompletedRef.current
                ) {

                    autoSubmittingRef.current = (
                        false
                    );
                }
            }

        },
        [
            attemptId,
            onSubmitted
        ]
    );


    useEffect(
        () => {

            if (
                !attempt?.expires_at ||
                attempt.status !==
                "in_progress"
            ) {

                return;
            }


            const calculateRemainingTime = () => {

                let expiryValue = (
                    attempt.expires_at
                );


                const hasTimezone = (
                    expiryValue.endsWith("Z") ||
                    /[+-]\d{2}:\d{2}$/.test(
                        expiryValue
                    )
                );


                if (!hasTimezone) {

                    expiryValue += "Z";
                }


                const expiryTime = (
                    new Date(
                        expiryValue
                    ).getTime()
                );


                const currentTime = (
                    Date.now()
                );


                const difference = (
                    expiryTime -
                    currentTime
                );


                return Math.max(
                    0,
                    Math.ceil(
                        difference / 1000
                    )
                );
            };


            const updateTimer = () => {

                const seconds = (
                    calculateRemainingTime()
                );


                setRemainingSeconds(
                    seconds
                );


                if (
                    seconds <= 0 &&
                    !submissionCompletedRef.current &&
                    !autoSubmittingRef.current
                ) {

                    submitQuiz(
                        true
                    );
                }
            };


            updateTimer();


            const timerId = setInterval(
                updateTimer,
                1000
            );


            return () => {

                clearInterval(
                    timerId
                );
            };

        },
        [
            attempt,
            submitQuiz
        ]
    );


    const saveAnswer = async (
        questionId,
        answer
    ) => {

        if (
            remainingSeconds !== null &&
            remainingSeconds <= 0
        ) {

            return;
        }


        if (
            submissionCompletedRef.current ||
            autoSubmittingRef.current
        ) {

            return;
        }


        const previousAnswer = (
            answersRef.current[
                questionId
            ]
        );


        const updatedAnswers = {
            ...answersRef.current,
            [questionId]: answer
        };


        answersRef.current = (
            updatedAnswers
        );

        setAnswers(
            updatedAnswers
        );


        try {

            setSavingQuestionId(
                questionId
            );

            setError("");


            await saveAttemptAnswer(
                attemptId,
                questionId,
                answer
            );


        } catch (err) {

            const revertedAnswers = {
                ...answersRef.current
            };


            if (
                previousAnswer === undefined
            ) {

                delete revertedAnswers[
                    questionId
                ];

            } else {

                revertedAnswers[
                    questionId
                ] = previousAnswer;
            }


            answersRef.current = (
                revertedAnswers
            );

            setAnswers(
                revertedAnswers
            );


            setError(
                err.message ||
                "Failed to save answer."
            );


        } finally {

            setSavingQuestionId(
                null
            );
        }
    };


    const handleSingleAnswerChange = (
        questionId,
        answer
    ) => {

        saveAnswer(
            questionId,
            answer
        );
    };


    const handleMultipleSelectChange = (
        questionId,
        option
    ) => {

        const currentAnswer = (
            Array.isArray(
                answersRef.current[
                    questionId
                ]
            )
                ? answersRef.current[
                    questionId
                ]
                : []
        );


        const isSelected = (
            currentAnswer.includes(
                option
            )
        );


        const updatedAnswer = (
            isSelected
                ? currentAnswer.filter(
                    answer =>
                        answer !== option
                )
                : [
                    ...currentAnswer,
                    option
                ]
        );


        if (
            updatedAnswer.length === 0
        ) {

            const updatedAnswers = {
                ...answersRef.current
            };


            delete updatedAnswers[
                questionId
            ];


            answersRef.current = (
                updatedAnswers
            );

            setAnswers(
                updatedAnswers
            );


            return;
        }


        saveAnswer(
            questionId,
            updatedAnswer
        );
    };


    const handleShortAnswerChange = (
        questionId,
        value
    ) => {

        const updatedAnswers = {
            ...answersRef.current
        };


        if (value.trim()) {

            updatedAnswers[
                questionId
            ] = value;

        } else {

            delete updatedAnswers[
                questionId
            ];
        }


        answersRef.current = (
            updatedAnswers
        );

        setAnswers(
            updatedAnswers
        );


        if (
            shortAnswerTimersRef.current[
                questionId
            ]
        ) {

            clearTimeout(
                shortAnswerTimersRef.current[
                    questionId
                ]
            );
        }


        if (!value.trim()) {

            return;
        }


        shortAnswerTimersRef.current[
            questionId
        ] = setTimeout(
            () => {

                saveAnswer(
                    questionId,
                    value
                );

            },
            500
        );
    };


    const handleShortAnswerBlur = (
        questionId
    ) => {

        const answer = (
            answersRef.current[
                questionId
            ]
        );


        if (
            typeof answer !== "string" ||
            !answer.trim()
        ) {

            return;
        }


        if (
            shortAnswerTimersRef.current[
                questionId
            ]
        ) {

            clearTimeout(
                shortAnswerTimersRef.current[
                    questionId
                ]
            );
        }


        saveAnswer(
            questionId,
            answer
        );
    };


    const handlePrevious = () => {

        setCurrentQuestionIndex(
            previousIndex => Math.max(
                0,
                previousIndex - 1
            )
        );
    };


    const handleNext = () => {

        const totalQuestions = (
            attempt?.question_snapshot
                ?.length || 0
        );


        setCurrentQuestionIndex(
            previousIndex => Math.min(
                totalQuestions - 1,
                previousIndex + 1
            )
        );
    };


    const isQuestionAnswered = (
        question
    ) => {

        const answer = (
            answers[
                question.id
            ]
        );


        if (
            question.question_type ===
            "multiple_select"
        ) {

            return (
                Array.isArray(answer) &&
                answer.length > 0
            );
        }


        if (
            question.question_type ===
            "short_answer"
        ) {

            return (
                typeof answer === "string" &&
                Boolean(
                    answer.trim()
                )
            );
        }


        return (
            typeof answer === "string" &&
            Boolean(answer)
        );
    };


    const handleSubmit = async () => {

        const totalQuestions = (
            attempt?.question_snapshot
                ?.length || 0
        );


        const answeredQuestions = (
            attempt.question_snapshot.filter(
                question =>
                    isQuestionAnswered(
                        question
                    )
            ).length
        );


        const unansweredQuestions = (
            totalQuestions -
            answeredQuestions
        );


        const confirmationMessage = (
            unansweredQuestions > 0
                ? (
                    `You have ${unansweredQuestions} ` +
                    "unanswered question(s). " +
                    "Do you still want to submit?"
                )
                : (
                    "Are you sure you want " +
                    "to submit this quiz?"
                )
        );


        const confirmed = window.confirm(
            confirmationMessage
        );


        if (!confirmed) {

            return;
        }


        await submitQuiz(
            false
        );
    };


    const formatTime = (
        totalSeconds
    ) => {

        if (
            totalSeconds === null
        ) {

            return "--:--";
        }


        const minutes = Math.floor(
            totalSeconds / 60
        );


        const seconds = (
            totalSeconds % 60
        );


        return (
            `${String(minutes).padStart(
                2,
                "0"
            )}:${String(seconds).padStart(
                2,
                "0"
            )}`
        );
    };


    const getQuestionTypeLabel = (
        questionType
    ) => {

        if (
            questionType ===
            "true_false"
        ) {

            return "True / False";
        }


        if (
            questionType ===
            "short_answer"
        ) {

            return "Short Answer";
        }


        if (
            questionType ===
            "multiple_select"
        ) {

            return "Multiple Select";
        }


        return "MCQ";
    };


    const renderSingleChoiceOptions = (
        question
    ) => {

        return question.options.map(
            (
                option,
                optionIndex
            ) => {

                const isSelected = (
                    answers[
                        question.id
                    ] === option
                );


                return (

                    <label
                        key={
                            `${question.id}-${optionIndex}`
                        }
                        className={
                            isSelected
                                ? (
                                    "answer-option " +
                                    "selected"
                                )
                                : "answer-option"
                        }
                    >

                        <input
                            type="radio"
                            name={
                                question.id
                            }
                            value={
                                option
                            }
                            checked={
                                isSelected
                            }
                            disabled={
                                savingQuestionId ===
                                question.id ||
                                submitting ||
                                isTimeExpired
                            }
                            onChange={
                                () =>
                                    handleSingleAnswerChange(
                                        question.id,
                                        option
                                    )
                            }
                        />


                        <span
                            className={
                                "option-indicator"
                            }
                        />


                        <span className="option-text">

                            {option}

                        </span>

                    </label>
                );
            }
        );
    };


    const renderMultipleSelectOptions = (
        question
    ) => {

        const selectedAnswers = (
            Array.isArray(
                answers[
                    question.id
                ]
            )
                ? answers[
                    question.id
                ]
                : []
        );


        return question.options.map(
            (
                option,
                optionIndex
            ) => {

                const isSelected = (
                    selectedAnswers.includes(
                        option
                    )
                );


                return (

                    <label
                        key={
                            `${question.id}-${optionIndex}`
                        }
                        className={
                            isSelected
                                ? (
                                    "answer-option " +
                                    "selected"
                                )
                                : "answer-option"
                        }
                    >

                        <input
                            type="checkbox"
                            value={option}
                            checked={
                                isSelected
                            }
                            disabled={
                                savingQuestionId ===
                                question.id ||
                                submitting ||
                                isTimeExpired
                            }
                            onChange={
                                () =>
                                    handleMultipleSelectChange(
                                        question.id,
                                        option
                                    )
                            }
                        />


                        <span
                            className={
                                "option-indicator"
                            }
                        />


                        <span className="option-text">

                            {option}

                        </span>

                    </label>
                );
            }
        );
    };


    const renderShortAnswer = (
        question
    ) => {

        const answer = (
            typeof answers[
                question.id
            ] === "string"
                ? answers[
                    question.id
                ]
                : ""
        );


        return (

            <div className="short-answer-container">

                <label
                    htmlFor={
                        `short-answer-${question.id}`
                    }
                    className="short-answer-label"
                >

                    Your Answer

                </label>


                <textarea
                    id={
                        `short-answer-${question.id}`
                    }
                    className={
                        "form-input " +
                        "short-answer-input"
                    }
                    value={answer}
                    rows={5}
                    placeholder={
                        "Type your answer here..."
                    }
                    disabled={
                        submitting ||
                        isTimeExpired
                    }
                    onChange={
                        event =>
                            handleShortAnswerChange(
                                question.id,
                                event.target.value
                            )
                    }
                    onBlur={
                        () =>
                            handleShortAnswerBlur(
                                question.id
                            )
                    }
                />

            </div>
        );
    };


    if (loading) {

        return (

            <div className="management-loading">

                Loading quiz attempt...

            </div>
        );
    }


    if (
        error &&
        !attempt
    ) {

        return (

            <div className="error-message">

                {error}

            </div>
        );
    }


    if (
        !attempt ||
        !Array.isArray(
            attempt.question_snapshot
        )
    ) {

        return (

            <div className="error-message">

                Unable to load quiz questions.

            </div>
        );
    }


    const questions = (
        attempt.question_snapshot
    );


    if (
        questions.length === 0
    ) {

        return (

            <div className="empty-state">

                <FaClipboardCheck
                    className="empty-state-icon"
                />

                <h3>
                    No questions available
                </h3>

                <p>
                    This quiz does not contain
                    any questions yet.
                </p>

            </div>
        );
    }


    const currentQuestion = (
        questions[
            currentQuestionIndex
        ]
    );


    const answeredCount = (
        questions.filter(
            question =>
                isQuestionAnswered(
                    question
                )
        ).length
    );


    const progressPercentage = (
        (
            answeredCount /
            questions.length
        ) * 100
    );


    const isTimeCritical = (
        remainingSeconds !== null &&
        remainingSeconds <= 60
    );


    const isTimeExpired = (
        remainingSeconds !== null &&
        remainingSeconds <= 0
    );


    return (

        <div className="quiz-attempt-page">

            {
                error && (

                    <div className="error-message">

                        {error}

                    </div>
                )
            }


            <div className="quiz-attempt-header">

                <div>

                    <h2>
                        Quiz Attempt
                    </h2>

                    <p>

                        Question {
                            currentQuestionIndex + 1
                        } of {
                            questions.length
                        } · {
                            answeredCount
                        } answered

                    </p>

                </div>


                <div
                    className={
                        isTimeExpired
                            ? "quiz-timer danger"
                            : isTimeCritical
                                ? "quiz-timer warning"
                                : "quiz-timer"
                    }
                >

                    <FaClock />


                    <span>

                        {
                            isTimeExpired
                                ? "Time Expired"
                                : formatTime(
                                    remainingSeconds
                                )
                        }

                    </span>

                </div>

            </div>


            <div className="quiz-progress-section">

                <div className="quiz-progress-info">

                    <span>

                        Question {
                            currentQuestionIndex + 1
                        } of {
                            questions.length
                        }

                    </span>


                    <span>

                        {answeredCount} of {
                            questions.length
                        } answered

                    </span>

                </div>


                <div className="quiz-progress-bar">

                    <div
                        className="quiz-progress-fill"
                        style={{
                            width:
                                `${progressPercentage}%`
                        }}
                    />

                </div>

            </div>


            <article className="quiz-question-card">

                <div className="question-meta">

                    <span className="question-number">

                        Question {
                            currentQuestionIndex + 1
                        }

                    </span>


                    <span
                        className={
                            `difficulty-badge ${
                                currentQuestion
                                    .difficulty ||
                                "easy"
                            }`
                        }
                    >

                        {
                            currentQuestion
                                .difficulty ||
                            "easy"
                        }

                    </span>

                </div>


                <h2 className="question-text">

                    {
                        currentQuestion.question
                    }

                </h2>


                <span className="question-type-label">

                    {
                        getQuestionTypeLabel(
                            currentQuestion
                                .question_type
                        )
                    }

                </span>


                <div className="answer-options">

                    {
                        currentQuestion.question_type ===
                        "short_answer"
                            ? renderShortAnswer(
                                currentQuestion
                            )
                            : currentQuestion.question_type ===
                                "multiple_select"
                                ? renderMultipleSelectOptions(
                                    currentQuestion
                                )
                                : renderSingleChoiceOptions(
                                    currentQuestion
                                )
                    }

                </div>


                {
                    savingQuestionId ===
                    currentQuestion.id && (

                        <p
                            className={
                                "answer-save-status saving"
                            }
                        >

                            Saving answer...

                        </p>
                    )
                }

            </article>


            <div className="quiz-navigation">

                <button
                    type="button"
                    className="quiz-nav-button"
                    disabled={
                        currentQuestionIndex === 0 ||
                        submitting ||
                        isTimeExpired
                    }
                    onClick={
                        handlePrevious
                    }
                >

                    <FaArrowLeft />

                    Previous

                </button>


                {
                    currentQuestionIndex <
                    questions.length - 1
                        ? (

                            <button
                                type="button"
                                className="quiz-nav-button"
                                disabled={
                                    submitting ||
                                    isTimeExpired
                                }
                                onClick={
                                    handleNext
                                }
                            >

                                Next

                                <FaArrowRight />

                            </button>

                        ) : (

                            <button
                                type="button"
                                className="submit-quiz-button"
                                disabled={
                                    submitting ||
                                    savingQuestionId !==
                                    null ||
                                    isTimeExpired
                                }
                                onClick={
                                    handleSubmit
                                }
                            >

                                <FaClipboardCheck />

                                {
                                    submitting
                                        ? "Submitting..."
                                        : "Submit Quiz"
                                }

                            </button>
                        )
                }

            </div>


            <div className="question-navigation-grid">

                {
                    questions.map(
                        (
                            question,
                            index
                        ) => {

                            const isAnswered = (
                                isQuestionAnswered(
                                    question
                                )
                            );


                            const isCurrent = (
                                index ===
                                currentQuestionIndex
                            );


                            let className = (
                                "question-navigation-button"
                            );


                            if (isAnswered) {

                                className += (
                                    " answered"
                                );
                            }


                            if (isCurrent) {

                                className += (
                                    " current"
                                );
                            }


                            return (

                                <button
                                    key={
                                        question.id
                                    }
                                    type="button"
                                    className={
                                        className
                                    }
                                    disabled={
                                        submitting ||
                                        isTimeExpired
                                    }
                                    onClick={
                                        () =>
                                            setCurrentQuestionIndex(
                                                index
                                            )
                                    }
                                >

                                    {index + 1}

                                </button>
                            );
                        }
                    )
                }

            </div>

        </div>
    );
}


export default QuizAttempt;