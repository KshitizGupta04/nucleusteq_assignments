import {
    useEffect,
    useMemo,
    useState
} from "react";

import {
    FaArrowLeft,
    FaBook,
    FaCalendarAlt,
    FaClock,
    FaPlay,
    FaRedoAlt,
    FaStar
} from "react-icons/fa";

import {
    getCategories,
    getQuizzes,
    startAttempt
} from "../../services/studentService";


function AvailableQuizzes({
    selectedCategory,
    onBackToCategories,
    onStartAttempt,
    onResumeAttempt,
    pendingAttemptId,
    pendingAttemptQuizId
}) {

    const [
        quizzes,
        setQuizzes
    ] = useState([]);

    const [
        categories,
        setCategories
    ] = useState([]);

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        error,
        setError
    ] = useState("");

    const [
        startingQuizId,
        setStartingQuizId
    ] = useState(null);


    useEffect(
        () => {

            const loadData = async () => {

                try {

                    setLoading(true);

                    setError("");


                    const [
                        quizData,
                        categoryData
                    ] = await Promise.all([
                        getQuizzes(),
                        getCategories()
                    ]);


                    setQuizzes(
                        Array.isArray(
                            quizData
                        )
                            ? quizData
                            : []
                    );


                    setCategories(
                        Array.isArray(
                            categoryData
                        )
                            ? categoryData
                            : []
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load quizzes."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadData();

        },
        []
    );


    const categoryMap = useMemo(
        () => {

            const map = {};


            categories.forEach(
                category => {

                    map[
                        category.id
                    ] = category.name;
                }
            );


            return map;

        },
        [
            categories
        ]
    );


    const filteredQuizzes = useMemo(
        () => {

            if (
                !selectedCategory?.id
            ) {

                return quizzes;
            }


            return quizzes.filter(
                quiz =>
                    quiz.category_id ===
                    selectedCategory.id
            );

        },
        [
            quizzes,
            selectedCategory
        ]
    );


    const parseBackendDate = (
        value
    ) => {

        if (!value) {

            return null;
        }


        const date = new Date(
            value
        );


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {

            return null;
        }


        return date;
    };


    const getQuizAvailability = (
        quiz
    ) => {

        const now = new Date();


        const availableFrom = (
            parseBackendDate(
                quiz.available_from
            )
        );


        const availableUntil = (
            parseBackendDate(
                quiz.available_until
            )
        );


        if (
            availableFrom &&
            now < availableFrom
        ) {

            return {
                status: "upcoming",
                label: "Upcoming",
                canStart: false
            };
        }


        if (
            availableUntil &&
            now > availableUntil
        ) {

            return {
                status: "expired",
                label: "Expired",
                canStart: false
            };
        }


        return {
            status: "available",
            label: "Available Now",
            canStart: true
        };
    };


    const formatDateTime = (
        value
    ) => {

        const date = parseBackendDate(
            value
        );


        if (!date) {

            return "Not specified";
        }


        return date.toLocaleString(
            "en-IN",
            {
                day: "2-digit",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                hour12: true
            }
        );
    };


    const handleStartQuiz = async (
        quiz
    ) => {

        if (
            pendingAttemptId &&
            pendingAttemptQuizId !== quiz.id
        ) {

            setError(
                "You already have an active quiz. " +
                "Resume that quiz before starting " +
                "another one."
            );

            return;
        }


        try {

            setStartingQuizId(
                quiz.id
            );

            setError("");


            const response = (
                await startAttempt(
                    quiz.id
                )
            );


            if (
                !response.attempt_id
            ) {

                throw new Error(
                    "Attempt ID was not returned."
                );
            }


            onStartAttempt(
                response.attempt_id,
                Boolean(
                    response.resumed
                ),
                quiz.id
            );

        } catch (err) {

            setError(
                err.message ||
                "Failed to start attempt."
            );

        } finally {

            setStartingQuizId(
                null
            );
        }
    };


    const handleResumeQuiz = (
        quiz
    ) => {

        if (
            !pendingAttemptId
        ) {

            setError(
                "Active attempt could not be found."
            );

            return;
        }


        setError("");


        onResumeAttempt(
            pendingAttemptId,
            quiz.id
        );
    };


    if (loading) {

        return (

            <div className="management-loading">

                Loading available quizzes...

            </div>
        );
    }


    return (

        <div className="quiz-list-page">

            <div
                className={
                    "student-category-navigation"
                }
            >

                {
                    onBackToCategories && (

                        <button
                            type="button"
                            className={
                                "back-to-categories-button"
                            }
                            onClick={
                                onBackToCategories
                            }
                        >

                            <FaArrowLeft />

                            <span>
                                Back to Categories
                            </span>

                        </button>
                    )
                }


                {
                    selectedCategory && (

                        <div
                            className={
                                "selected-category-summary"
                            }
                        >

                            <div
                                className={
                                    "selected-category-summary-icon"
                                }
                            >

                                <FaBook />

                            </div>


                            <div>

                                <h2>
                                    {
                                        selectedCategory.name
                                    }
                                </h2>

                                <p>
                                    {
                                        selectedCategory.description
                                    }
                                </p>

                            </div>

                        </div>
                    )
                }

            </div>


            {
                error && (

                    <div className="error-message">

                        {error}

                    </div>
                )
            }


            {
                filteredQuizzes.length === 0
                    ? (

                        <div className="empty-state">

                            <FaBook
                                className={
                                    "empty-state-icon"
                                }
                            />

                            <h3>
                                No quizzes available
                            </h3>

                            <p>

                                {
                                    selectedCategory
                                        ? (
                                            `There are currently no quizzes available in ${selectedCategory.name}.`
                                        )
                                        : (
                                            "There are currently no assessments available."
                                        )
                                }

                            </p>

                        </div>
                    )
                    : (

                        <div className="quiz-card-grid">

                            {
                                filteredQuizzes.map(
                                    quiz => {

                                        const availability = (
                                            getQuizAvailability(
                                                quiz
                                            )
                                        );


                                        const remainingAttempts = (
                                            quiz.remaining_attempts ??
                                            quiz.max_attempts ??
                                            0
                                        );


                                        const maxAttempts = (
                                            quiz.max_attempts ??
                                            0
                                        );


                                        const noAttemptsLeft = (
                                            remainingAttempts <= 0
                                        );


                                        const isPendingQuiz = (
                                            Boolean(
                                                pendingAttemptId
                                            ) &&
                                            pendingAttemptQuizId ===
                                            quiz.id
                                        );


                                        const anotherQuizIsPending = (
                                            Boolean(
                                                pendingAttemptId
                                            ) &&
                                            pendingAttemptQuizId !==
                                            quiz.id
                                        );


                                        const isStarting = (
                                            startingQuizId ===
                                            quiz.id
                                        );


                                        return (

                                            <article
                                                key={
                                                    quiz.id
                                                }
                                                className={
                                                    "student-quiz-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "quiz-card-top-row"
                                                    }
                                                >

                                                    <div
                                                        className={
                                                            "quiz-card-header"
                                                        }
                                                    >

                                                        <FaBook />

                                                        <span>

                                                            {
                                                                categoryMap[
                                                                    quiz.category_id
                                                                ] ||
                                                                selectedCategory?.name ||
                                                                "Unknown Category"
                                                            }

                                                        </span>

                                                    </div>


                                                    <span
                                                        className={
                                                            (
                                                                "quiz-availability-badge " +
                                                                (
                                                                    isPendingQuiz
                                                                        ? "available"
                                                                        : availability.status
                                                                )
                                                            )
                                                        }
                                                    >

                                                        {
                                                            isPendingQuiz
                                                                ? "Active Attempt"
                                                                : availability.label
                                                        }

                                                    </span>

                                                </div>


                                                <h3>
                                                    {quiz.title}
                                                </h3>


                                                <p
                                                    className={
                                                        "quiz-description"
                                                    }
                                                >

                                                    {
                                                        quiz.description
                                                    }

                                                </p>


                                                <div
                                                    className={
                                                        "quiz-meta"
                                                    }
                                                >

                                                    <span>

                                                        <FaClock />

                                                        {
                                                            quiz.duration
                                                        } min

                                                    </span>


                                                    <span>

                                                        <FaStar />

                                                        {
                                                            quiz.total_marks
                                                        } marks

                                                    </span>

                                                </div>


                                                <div
                                                    className={
                                                        noAttemptsLeft
                                                            ? (
                                                                "quiz-attempt-info " +
                                                                "no-attempts"
                                                            )
                                                            : "quiz-attempt-info"
                                                    }
                                                >

                                                    <FaRedoAlt />

                                                    <span>

                                                        {
                                                            noAttemptsLeft
                                                                ? (
                                                                    "No attempts remaining"
                                                                )
                                                                : (
                                                                    <>
                                                                        <strong>
                                                                            {
                                                                                remainingAttempts
                                                                            }
                                                                        </strong>

                                                                        {" of "}

                                                                        {
                                                                            maxAttempts
                                                                        }

                                                                        {
                                                                            remainingAttempts === 1
                                                                                ? " attempt remaining"
                                                                                : " attempts remaining"
                                                                        }
                                                                    </>
                                                                )
                                                        }

                                                    </span>

                                                </div>


                                                {
                                                    (
                                                        quiz.available_from ||
                                                        quiz.available_until
                                                    ) && (

                                                        <div
                                                            className={
                                                                "quiz-schedule-info"
                                                            }
                                                        >

                                                            <div>

                                                                <FaCalendarAlt />

                                                                <span>

                                                                    <strong>
                                                                        From:
                                                                    </strong>

                                                                    {" "}

                                                                    {
                                                                        formatDateTime(
                                                                            quiz.available_from
                                                                        )
                                                                    }

                                                                </span>

                                                            </div>


                                                            <div>

                                                                <FaCalendarAlt />

                                                                <span>

                                                                    <strong>
                                                                        Until:
                                                                    </strong>

                                                                    {" "}

                                                                    {
                                                                        formatDateTime(
                                                                            quiz.available_until
                                                                        )
                                                                    }

                                                                </span>

                                                            </div>

                                                        </div>
                                                    )
                                                }


                                                {
                                                    isPendingQuiz
                                                        ? (

                                                            <button
                                                                type="button"
                                                                className={
                                                                    "primary-button"
                                                                }
                                                                onClick={
                                                                    () =>
                                                                        handleResumeQuiz(
                                                                            quiz
                                                                        )
                                                                }
                                                            >

                                                                <FaRedoAlt />

                                                                Resume Quiz

                                                            </button>

                                                        )
                                                        : (

                                                            <button
                                                                type="button"
                                                                className={
                                                                    "primary-button"
                                                                }
                                                                disabled={
                                                                    !availability.canStart ||
                                                                    noAttemptsLeft ||
                                                                    isStarting ||
                                                                    anotherQuizIsPending
                                                                }
                                                                onClick={
                                                                    () =>
                                                                        handleStartQuiz(
                                                                            quiz
                                                                        )
                                                                }
                                                            >

                                                                <FaPlay />

                                                                {
                                                                    isStarting
                                                                        ? " Starting..."
                                                                        : anotherQuizIsPending
                                                                            ? " Another Quiz Active"
                                                                            : noAttemptsLeft
                                                                                ? " Maximum Attempts Reached"
                                                                                : availability.status ===
                                                                                    "upcoming"
                                                                                    ? " Not Started Yet"
                                                                                    : availability.status ===
                                                                                        "expired"
                                                                                        ? " Quiz Expired"
                                                                                        : " Start Quiz"
                                                                }

                                                            </button>
                                                        )
                                                }

                                            </article>
                                        );
                                    }
                                )
                            }

                        </div>
                    )
            }

        </div>
    );
}


export default AvailableQuizzes;