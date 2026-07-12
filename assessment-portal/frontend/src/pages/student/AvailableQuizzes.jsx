import {
    useEffect,
    useMemo,
    useState
} from "react";

import {
    FaBook,
    FaClock,
    FaPlay,
    FaStar
} from "react-icons/fa";

import {
    getCategories,
    getQuizzes,
    startAttempt
} from "../../services/api";


function AvailableQuizzes({
    onStartAttempt
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
                        Array.isArray(quizData)
                            ? quizData
                            : []
                    );

                    setCategories(
                        Array.isArray(categoryData)
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

                    map[category.id] = (
                        category.name
                    );
                }
            );

            return map;

        },
        [
            categories
        ]
    );


    const handleStartQuiz = async (
        quizId
    ) => {

        try {

            setStartingQuizId(
                quizId
            );

            setError("");

            const response = (
                await startAttempt(
                    quizId
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
                response.resumed
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


    if (loading) {

        return (

            <div className="management-loading">

                Loading available quizzes...

            </div>
        );
    }


    return (

        <div className="quiz-list-page">

            {
                error && (

                    <div className="error-message">

                        {error}

                    </div>
                )
            }


            {
                quizzes.length === 0
                    ? (

                        <div className="empty-state">

                            <FaBook
                                className="empty-state-icon"
                            />

                            <h3>
                                No quizzes available
                            </h3>

                            <p>
                                There are currently no
                                assessments available.
                            </p>

                        </div>
                    )
                    : (

                        <div className="quiz-card-grid">

                            {
                                quizzes.map(
                                    quiz => (

                                        <article
                                            key={quiz.id}
                                            className="student-quiz-card"
                                        >

                                            <div className="quiz-card-header">

                                                <FaBook />

                                                <span>
                                                    {
                                                        categoryMap[
                                                            quiz.category_id
                                                        ] ||
                                                        "Unknown Category"
                                                    }
                                                </span>

                                            </div>


                                            <h3>
                                                {quiz.title}
                                            </h3>


                                            <p className="quiz-description">

                                                {
                                                    quiz.description
                                                }

                                            </p>


                                            <div className="quiz-meta">

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


                                            <button
                                                type="button"
                                                className="primary-button"
                                                disabled={
                                                    startingQuizId ===
                                                    quiz.id
                                                }
                                                onClick={
                                                    () =>
                                                        handleStartQuiz(
                                                            quiz.id
                                                        )
                                                }
                                            >

                                                <FaPlay />

                                                {
                                                    startingQuizId ===
                                                    quiz.id
                                                        ? " Starting..."
                                                        : " Start Quiz"
                                                }

                                            </button>

                                        </article>
                                    )
                                )
                            }

                        </div>
                    )
            }

        </div>
    );
}


export default AvailableQuizzes;