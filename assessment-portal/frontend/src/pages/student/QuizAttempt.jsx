import {
    useCallback,
    useEffect,
    useRef,
    useState
} from "react";

import {
    FaArrowLeft,
    FaArrowRight,
    FaCheck,
    FaClipboardCheck,
    FaClock
} from "react-icons/fa";

import {
    resumeAttempt,
    saveAttemptAnswer,
    submitAttempt
} from "../../services/api";


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
        ]
    );


    const submitQuiz = useCallback(
        async (
            isAutoSubmit = false
        ) => {

            if (
                submitting ||
                autoSubmittingRef.current
            ) {

                return;
            }


            if (isAutoSubmit) {

                autoSubmittingRef.current = true;
            }


            try {

                setSubmitting(true);

                setError("");

                await submitAttempt(
                    attemptId,
                    answersRef.current
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

                    onSubmitted();

                    return;
                }

                setError(
                    isAutoSubmit
                        ? (
                            "Time expired. " +
                            message
                        )
                        : message
                );

            } finally {

                setSubmitting(false);

                if (!isAutoSubmit) {

                    autoSubmittingRef.current = (
                        false
                    );
                }
            }

        },
        [
            attemptId,
            onSubmitted,
            submitting
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


    const handleAnswerChange = async (
        questionId,
        answer
    ) => {

        if (
            remainingSeconds !== null &&
            remainingSeconds <= 0
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
                previousAnswer ===
                undefined
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


    const handleSubmit = async () => {

        const totalQuestions = (
            attempt?.question_snapshot
                ?.length || 0
        );

        const answeredQuestions = (
            Object.keys(
                answersRef.current
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
        Object.keys(
            answers
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


            <div className="attempt-summary">

                <div>

                    <span className="attempt-progress-label">

                        Question {
                            currentQuestionIndex + 1
                        } of {
                            questions.length
                        }

                    </span>

                    <p>

                        {
                            answeredCount
                        } of {
                            questions.length
                        } answered

                    </p>

                </div>


                <div className="attempt-summary-right">

                    <div
                        className={
                            isTimeCritical
                                ? (
                                    "attempt-timer " +
                                    "time-critical"
                                )
                                : "attempt-timer"
                        }
                    >

                        <FaClock />

                        <span>

                            {
                                isTimeExpired
                                    ? (
                                        "Time Expired"
                                    )
                                    : (
                                        formatTime(
                                            remainingSeconds
                                        )
                                    )
                            }

                        </span>

                    </div>


                    <span className="attempt-status">

                        {
                            submitting &&
                            isTimeExpired
                                ? "Auto-submitting..."
                                : attempt.status
                        }

                    </span>

                </div>

            </div>


            <div className="attempt-progress-bar">

                <div
                    className="attempt-progress-fill"
                    style={{
                        width:
                            `${progressPercentage}%`
                    }}
                />

            </div>


            <article className="attempt-question-card">

                <div className="question-heading">

                    <span className="question-number">

                        {
                            currentQuestionIndex + 1
                        }

                    </span>

                    <h2>

                        {
                            currentQuestion.question
                        }

                    </h2>

                </div>


                <div className="question-options">

                    {
                        currentQuestion.options.map(
                            (
                                option,
                                optionIndex
                            ) => {

                                const isSelected = (
                                    answers[
                                        currentQuestion.id
                                    ] === option
                                );

                                return (

                                    <label
                                        key={
                                            `${currentQuestion.id}-${optionIndex}`
                                        }
                                        className={
                                            isSelected
                                                ? (
                                                    "question-option " +
                                                    "selected"
                                                )
                                                : (
                                                    "question-option"
                                                )
                                        }
                                    >

                                        <input
                                            type="radio"
                                            name={
                                                currentQuestion.id
                                            }
                                            value={
                                                option
                                            }
                                            checked={
                                                isSelected
                                            }
                                            disabled={
                                                savingQuestionId ===
                                                currentQuestion.id ||
                                                submitting ||
                                                isTimeExpired
                                            }
                                            onChange={
                                                () =>
                                                    handleAnswerChange(
                                                        currentQuestion.id,
                                                        option
                                                    )
                                            }
                                        />

                                        <span className="option-letter">

                                            {
                                                String.fromCharCode(
                                                    65 +
                                                    optionIndex
                                                )
                                            }

                                        </span>

                                        <span className="option-text">

                                            {option}

                                        </span>


                                        {
                                            isSelected && (

                                                <FaCheck
                                                    className={
                                                        "option-check"
                                                    }
                                                />

                                            )
                                        }

                                    </label>
                                );
                            }
                        )
                    }

                </div>


                {
                    savingQuestionId ===
                    currentQuestion.id && (

                        <p className="answer-saving-message">

                            Saving answer...

                        </p>
                    )
                }

            </article>


            <div className="attempt-navigation">

                <button
                    type="button"
                    className="secondary-button"
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
                                className="primary-button"
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
                        )
                        : (

                            <button
                                type="button"
                                className={
                                    "primary-button " +
                                    "submit-attempt-button"
                                }
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
                                answers[
                                    question.id
                                ] !== undefined
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