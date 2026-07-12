import {
    useEffect,
    useState
} from "react";

import {
    FaArrowLeft,
    FaCheckCircle,
    FaClipboardCheck,
    FaTimesCircle
} from "react-icons/fa";

import {
    getResultById
} from "../../services/api";


function ResultBreakdown({
    resultId,
    onBack
}) {

    const [
        result,
        setResult
    ] = useState(null);

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

            const loadResult = async () => {

                if (!resultId) {

                    setError(
                        "Result ID is missing."
                    );

                    setLoading(false);

                    return;
                }


                try {

                    setLoading(true);

                    setError("");

                    const data = (
                        await getResultById(
                            resultId
                        )
                    );

                    setResult(
                        data
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load result."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadResult();

        },
        [
            resultId
        ]
    );


    const formatNumber = (
        value
    ) => {

        const numericValue = Number(
            value
        );

        if (
            Number.isNaN(
                numericValue
            )
        ) {

            return "0";
        }

        return Number.isInteger(
            numericValue
        )
            ? numericValue
            : numericValue.toFixed(2);
    };


    if (loading) {

        return (

            <div className="management-loading">

                Loading result breakdown...

            </div>
        );
    }


    if (
        error &&
        !result
    ) {

        return (

            <div>

                <div className="error-message">

                    {error}

                </div>


                <button
                    type="button"
                    className="secondary-button"
                    onClick={onBack}
                >

                    <FaArrowLeft />

                    Back to Results

                </button>

            </div>
        );
    }


    if (!result) {

        return null;
    }


    const isPassed = (
        result.status === "pass"
    );

    const questionBreakdown = (
        Array.isArray(
            result.question_breakdown
        )
            ? result.question_breakdown
            : []
    );


    return (

        <div className="result-breakdown-page">

            <button
                type="button"
                className={
                    "secondary-button " +
                    "result-back-button"
                }
                onClick={onBack}
            >

                <FaArrowLeft />

                Back to Results

            </button>


            {
                error && (

                    <div className="error-message">

                        {error}

                    </div>
                )
            }


            <section className="result-summary-card">

                <div className="result-summary-heading">

                    <div>

                        <span className="result-attempt-number">

                            Attempt {
                                result.attempt_number
                            }

                        </span>

                        <h2>
                            Quiz Result
                        </h2>

                    </div>


                    <span
                        className={
                            isPassed
                                ? (
                                    "result-status passed"
                                )
                                : (
                                    "result-status failed"
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


                <div className="result-summary-grid">

                    <div className="result-summary-item">

                        <span>
                            Score
                        </span>

                        <strong>

                            {
                                formatNumber(
                                    result.score_obtained
                                )
                            }

                            {" / "}

                            {
                                formatNumber(
                                    result.total_marks
                                )
                            }

                        </strong>

                    </div>


                    <div className="result-summary-item">

                        <span>
                            Percentage
                        </span>

                        <strong>

                            {
                                formatNumber(
                                    result.percentage
                                )
                            }%

                        </strong>

                    </div>


                    <div className="result-summary-item">

                        <span>
                            Questions
                        </span>

                        <strong>

                            {
                                questionBreakdown.length
                            }

                        </strong>

                    </div>

                </div>

            </section>


            <section className="result-questions-section">

                <div className="result-section-heading">

                    <FaClipboardCheck />

                    <h2>
                        Question Breakdown
                    </h2>

                </div>


                {
                    questionBreakdown.length === 0
                        ? (

                            <div className="empty-state">

                                <p>
                                    No question breakdown
                                    is available.
                                </p>

                            </div>
                        )
                        : (

                            <div className="breakdown-list">

                                {
                                    questionBreakdown.map(
                                        (
                                            item,
                                            index
                                        ) => (

                                            <article
                                                key={
                                                    item.question_id
                                                }
                                                className={
                                                    item.is_correct
                                                        ? (
                                                            "breakdown-card " +
                                                            "correct"
                                                        )
                                                        : (
                                                            "breakdown-card " +
                                                            "incorrect"
                                                        )
                                                }
                                            >

                                                <div
                                                    className={
                                                        "breakdown-question-header"
                                                    }
                                                >

                                                    <span
                                                        className={
                                                            "breakdown-question-number"
                                                        }
                                                    >

                                                        {index + 1}

                                                    </span>


                                                    <h3>

                                                        {
                                                            item.question
                                                        }

                                                    </h3>


                                                    <span
                                                        className={
                                                            item.is_correct
                                                                ? (
                                                                    "answer-result " +
                                                                    "correct"
                                                                )
                                                                : (
                                                                    "answer-result " +
                                                                    "incorrect"
                                                                )
                                                        }
                                                    >

                                                        {
                                                            item.is_correct
                                                                ? (
                                                                    <FaCheckCircle />
                                                                )
                                                                : (
                                                                    <FaTimesCircle />
                                                                )
                                                        }

                                                        {
                                                            item.is_correct
                                                                ? "Correct"
                                                                : "Incorrect"
                                                        }

                                                    </span>

                                                </div>


                                                <div
                                                    className={
                                                        "breakdown-answer-grid"
                                                    }
                                                >

                                                    <div
                                                        className={
                                                            "breakdown-answer"
                                                        }
                                                    >

                                                        <span>
                                                            Your Answer
                                                        </span>

                                                        <strong>

                                                            {
                                                                item.selected_answer ||
                                                                "Not answered"
                                                            }

                                                        </strong>

                                                    </div>


                                                    <div
                                                        className={
                                                            "breakdown-answer"
                                                        }
                                                    >

                                                        <span>
                                                            Correct Answer
                                                        </span>

                                                        <strong>

                                                            {
                                                                item.correct_answer
                                                            }

                                                        </strong>

                                                    </div>


                                                    <div
                                                        className={
                                                            "breakdown-answer"
                                                        }
                                                    >

                                                        <span>
                                                            Marks Obtained
                                                        </span>

                                                        <strong>

                                                            {
                                                                formatNumber(
                                                                    item.marks_obtained
                                                                )
                                                            }

                                                        </strong>

                                                    </div>

                                                </div>

                                            </article>
                                        )
                                    )
                                }

                            </div>
                        )
                }

            </section>

        </div>
    );
}


export default ResultBreakdown;