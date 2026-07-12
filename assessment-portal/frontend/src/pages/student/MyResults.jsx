import {
    useEffect,
    useMemo,
    useState
} from "react";

import {
    FaChartBar,
    FaCheckCircle,
    FaEye,
    FaTimesCircle
} from "react-icons/fa";

import {
    getMyResults,
    getQuizzes
} from "../../services/api";


function MyResults({
    onViewResult
}) {

    const [
        results,
        setResults
    ] = useState([]);

    const [
        quizzes,
        setQuizzes
    ] = useState([]);

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        error,
        setError
    ] = useState("");


    useEffect(
        () => {

            const loadResults = async () => {

                try {

                    setLoading(true);

                    setError("");

                    const [
                        resultData,
                        quizData
                    ] = await Promise.all([
                        getMyResults(),
                        getQuizzes()
                    ]);

                    setResults(
                        Array.isArray(
                            resultData
                        )
                            ? resultData
                            : []
                    );

                    setQuizzes(
                        Array.isArray(
                            quizData
                        )
                            ? quizData
                            : []
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load results."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadResults();

        },
        []
    );


    const quizMap = useMemo(
        () => {

            const map = {};

            quizzes.forEach(
                quiz => {

                    map[quiz.id] = (
                        quiz.title
                    );
                }
            );

            return map;

        },
        [
            quizzes
        ]
    );


    const formatPercentage = (
        percentage
    ) => {

        const numericPercentage = Number(
            percentage
        );

        if (
            Number.isNaN(
                numericPercentage
            )
        ) {

            return "0.00";
        }

        return numericPercentage.toFixed(
            2
        );
    };


    const formatScore = (
        score
    ) => {

        const numericScore = Number(
            score
        );

        if (
            Number.isNaN(
                numericScore
            )
        ) {

            return "0";
        }

        return Number.isInteger(
            numericScore
        )
            ? numericScore
            : numericScore.toFixed(2);
    };


    if (loading) {

        return (

            <div className="management-loading">

                Loading your results...

            </div>
        );
    }


    return (

        <div className="student-results-page">

            {
                error && (

                    <div className="error-message">

                        {error}

                    </div>
                )
            }


            {
                results.length === 0
                    ? (

                        <div className="empty-state">

                            <FaChartBar
                                className="empty-state-icon"
                            />

                            <h3>
                                No results available
                            </h3>

                            <p>
                                Complete a quiz to see
                                your results here.
                            </p>

                        </div>
                    )
                    : (

                        <div className="results-card-grid">

                            {
                                results.map(
                                    result => {

                                        const isPassed = (
                                            result.status ===
                                            "pass"
                                        );

                                        return (

                                            <article
                                                key={
                                                    result.result_id
                                                }
                                                className={
                                                    "student-result-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "result-card-header"
                                                    }
                                                >

                                                    <div>

                                                        <span
                                                            className={
                                                                "result-attempt-number"
                                                            }
                                                        >
                                                            Attempt {
                                                                result.attempt_number
                                                            }
                                                        </span>

                                                        <h3>

                                                            {
                                                                quizMap[
                                                                    result.quiz_id
                                                                ] ||
                                                                "Quiz"
                                                            }

                                                        </h3>

                                                    </div>


                                                    <span
                                                        className={
                                                            isPassed
                                                                ? (
                                                                    "result-status " +
                                                                    "passed"
                                                                )
                                                                : (
                                                                    "result-status " +
                                                                    "failed"
                                                                )
                                                        }
                                                    >

                                                        {
                                                            isPassed
                                                                ? (
                                                                    <FaCheckCircle />
                                                                )
                                                                : (
                                                                    <FaTimesCircle />
                                                                )
                                                        }

                                                        {
                                                            isPassed
                                                                ? "Pass"
                                                                : "Fail"
                                                        }

                                                    </span>

                                                </div>


                                                <div
                                                    className={
                                                        "result-score-section"
                                                    }
                                                >

                                                    <div>

                                                        <span>
                                                            Score
                                                        </span>

                                                        <strong>

                                                            {
                                                                formatScore(
                                                                    result.score_obtained
                                                                )
                                                            }

                                                            {" / "}

                                                            {
                                                                formatScore(
                                                                    result.total_marks
                                                                )
                                                            }

                                                        </strong>

                                                    </div>


                                                    <div>

                                                        <span>
                                                            Percentage
                                                        </span>

                                                        <strong>

                                                            {
                                                                formatPercentage(
                                                                    result.percentage
                                                                )
                                                            }%

                                                        </strong>

                                                    </div>

                                                </div>


                                                <button
                                                    type="button"
                                                    className={
                                                        "secondary-button " +
                                                        "view-result-button"
                                                    }
                                                    onClick={
                                                        () =>
                                                            onViewResult(
                                                                result.result_id
                                                            )
                                                    }
                                                >

                                                    <FaEye />

                                                    View Breakdown

                                                </button>

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


export default MyResults;