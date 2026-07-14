import {
    useCallback,
    useEffect,
    useState
} from "react";

import {
    FaChartBar,
    FaCheckCircle,
    FaCrown,
    FaMedal,
    FaPercentage,
    FaTimesCircle,
    FaTrophy,
    FaUsers
} from "react-icons/fa";

import {
    getQuizzes,
    getQuizLeaderboard,
    getQuizStatistics
} from "../../services/adminService";

import "../../styles/admin/quizAnalytics.css";

function QuizAnalytics() {

    const [
        quizzes,
        setQuizzes
    ] = useState([]);

    const [
        selectedQuizId,
        setSelectedQuizId
    ] = useState("");

    const [
        statistics,
        setStatistics
    ] = useState(null);

    const [
        leaderboard,
        setLeaderboard
    ] = useState([]);

    const [
        loadingQuizzes,
        setLoadingQuizzes
    ] = useState(true);

    const [
        loadingAnalytics,
        setLoadingAnalytics
    ] = useState(false);

    const [
        error,
        setError
    ] = useState("");


    const loadQuizzes = useCallback(
        async () => {

            try {

                setLoadingQuizzes(true);

                setError("");

                const data = await getQuizzes();

                const quizList = (
                    Array.isArray(data)
                        ? data
                        : []
                );

                setQuizzes(
                    quizList
                );

                if (
                    quizList.length > 0
                ) {

                    setSelectedQuizId(
                        currentQuizId => (
                            currentQuizId ||
                            quizList[0].id
                        )
                    );
                }

            } catch (err) {

                setError(
                    err.message ||
                    "Failed to load quizzes."
                );

            } finally {

                setLoadingQuizzes(false);
            }
        },
        []
    );


    const loadAnalytics = useCallback(
        async () => {

            if (!selectedQuizId) {

                setStatistics(null);

                setLeaderboard([]);

                return;
            }


            try {

                setLoadingAnalytics(true);

                setError("");


                const [
                    statisticsData,
                    leaderboardData
                ] = await Promise.all([
                    getQuizStatistics(
                        selectedQuizId
                    ),
                    getQuizLeaderboard(
                        selectedQuizId
                    )
                ]);


                setStatistics(
                    statisticsData
                );

                setLeaderboard(
                    Array.isArray(
                        leaderboardData
                    )
                        ? leaderboardData
                        : []
                );

            } catch (err) {

                setStatistics(null);

                setLeaderboard([]);

                setError(
                    err.message ||
                    "Failed to load quiz analytics."
                );

            } finally {

                setLoadingAnalytics(false);
            }
        },
        [
            selectedQuizId
        ]
    );


    useEffect(
        () => {

            loadQuizzes();

        },
        [
            loadQuizzes
        ]
    );


    useEffect(
        () => {

            loadAnalytics();

        },
        [
            loadAnalytics
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


    const getRankIcon = (
        rank
    ) => {

        if (rank === 1) {

            return <FaCrown />;
        }

        if (
            rank === 2 ||
            rank === 3
        ) {

            return <FaMedal />;
        }

        return rank;
    };


    if (loadingQuizzes) {

        return (

            <div className="management-loading">

                Loading quizzes...

            </div>
        );
    }


    return (

        <section className="quiz-analytics-page">

            <div className="management-header">

                <div>

                    <h2>
                        Quiz Analytics
                    </h2>

                    <p>
                        View quiz statistics,
                        performance and leaderboard.
                    </p>

                </div>


                <div className="analytics-quiz-selector">

                    <label htmlFor="analytics-quiz">

                        Select Quiz

                    </label>

                    <select
                        id="analytics-quiz"
                        value={selectedQuizId}
                        onChange={
                            event => {

                                setSelectedQuizId(
                                    event.target.value
                                );
                            }
                        }
                    >

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

            </div>


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

                            <FaChartBar
                                className={
                                    "empty-state-icon"
                                }
                            />

                            <h3>
                                No quizzes available
                            </h3>

                            <p>
                                Create a quiz to view
                                analytics and leaderboard.
                            </p>

                        </div>
                    )
                    : loadingAnalytics
                        ? (

                            <div className="management-loading">

                                Loading quiz analytics...

                            </div>
                        )
                        : (

                            <>

                                {
                                    statistics && (

                                        <div
                                            className={
                                                "analytics-stat-grid"
                                            }
                                        >

                                            <article
                                                className={
                                                    "analytics-stat-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "analytics-stat-icon"
                                                    }
                                                >

                                                    <FaUsers />

                                                </div>

                                                <div>

                                                    <span>
                                                        Total Attempts
                                                    </span>

                                                    <strong>

                                                        {
                                                            statistics
                                                                .total_attempts
                                                        }

                                                    </strong>

                                                </div>

                                            </article>


                                            <article
                                                className={
                                                    "analytics-stat-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "analytics-stat-icon"
                                                    }
                                                >

                                                    <FaChartBar />

                                                </div>

                                                <div>

                                                    <span>
                                                        Average Score
                                                    </span>

                                                    <strong>

                                                        {
                                                            formatNumber(
                                                                statistics
                                                                    .average_score
                                                            )
                                                        }

                                                    </strong>

                                                </div>

                                            </article>


                                            <article
                                                className={
                                                    "analytics-stat-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "analytics-stat-icon " +
                                                        "success"
                                                    }
                                                >

                                                    <FaCheckCircle />

                                                </div>

                                                <div>

                                                    <span>
                                                        Passed
                                                    </span>

                                                    <strong>

                                                        {
                                                            statistics
                                                                .pass_count
                                                        }

                                                    </strong>

                                                </div>

                                            </article>


                                            <article
                                                className={
                                                    "analytics-stat-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "analytics-stat-icon " +
                                                        "danger"
                                                    }
                                                >

                                                    <FaTimesCircle />

                                                </div>

                                                <div>

                                                    <span>
                                                        Failed
                                                    </span>

                                                    <strong>

                                                        {
                                                            statistics
                                                                .fail_count
                                                        }

                                                    </strong>

                                                </div>

                                            </article>


                                            <article
                                                className={
                                                    "analytics-stat-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "analytics-stat-icon"
                                                    }
                                                >

                                                    <FaPercentage />

                                                </div>

                                                <div>

                                                    <span>
                                                        Pass Rate
                                                    </span>

                                                    <strong>

                                                        {
                                                            formatNumber(
                                                                statistics
                                                                    .pass_rate
                                                            )
                                                        }%

                                                    </strong>

                                                </div>

                                            </article>

                                        </div>
                                    )
                                }


                                <section
                                    className={
                                        "leaderboard-section"
                                    }
                                >

                                    <div
                                        className={
                                            "leaderboard-heading"
                                        }
                                    >

                                        <div>

                                            <FaTrophy />

                                            <h2>
                                                Leaderboard
                                            </h2>

                                        </div>

                                        <span>

                                                {
                                                    leaderboard.length
                                                }

                                                {" "}

                                                {
                                                    leaderboard.length === 1
                                                        ? "Student"
                                                        : "Students"
                                                }

                                        </span>

                                    </div>


                                    {
                                        leaderboard.length === 0
                                            ? (

                                                <div
                                                    className={
                                                        "empty-state"
                                                    }
                                                >

                                                    <FaTrophy
                                                        className={
                                                            "empty-state-icon"
                                                        }
                                                    />

                                                    <h3>
                                                        No leaderboard data
                                                    </h3>

                                                    <p>
                                                        No submitted attempts
                                                        are available for this
                                                        quiz yet.
                                                    </p>

                                                </div>
                                            )
                                            : (

                                                <div
                                                    className={
                                                        "leaderboard-table-wrapper"
                                                    }
                                                >

                                                    <table
                                                        className={
                                                            "leaderboard-table"
                                                        }
                                                    >

                                                        <thead>

                                                            <tr>

                                                                <th>
                                                                    Rank
                                                                </th>

                                                                <th>
                                                                    Student
                                                                </th>

                                                                <th>
                                                                    Score
                                                                </th>

                                                                <th>
                                                                    Percentage
                                                                </th>

                                                            </tr>

                                                        </thead>


                                                        <tbody>

                                                            {
                                                                leaderboard.map(
                                                                    item => (

                                                                        <tr
                                                                            key={
                                                                                `${
                                                                                    item.student_id
                                                                                }-${
                                                                                    item.rank
                                                                                }`
                                                                            }
                                                                            className={
                                                                                item.rank <= 3
                                                                                    ? (
                                                                                        `top-rank rank-${
                                                                                            item.rank
                                                                                        }`
                                                                                    )
                                                                                    : ""
                                                                            }
                                                                        >

                                                                            <td>

                                                                                <span
                                                                                    className={
                                                                                        "leaderboard-rank"
                                                                                    }
                                                                                >

                                                                                    {
                                                                                        getRankIcon(
                                                                                            item.rank
                                                                                        )
                                                                                    }

                                                                                </span>

                                                                            </td>


                                                                            <td>

                                                                                <span
                                                                                    className={
                                                                                        "leaderboard-student"
                                                                                    }
                                                                                    title={
                                                                                        item.student_id
                                                                                    }
                                                                                >

                                                                                    {
                                                                                        item.student_id
                                                                                    }

                                                                                </span>

                                                                            </td>


                                                                            <td>

                                                                                <strong>

                                                                                    {
                                                                                        formatNumber(
                                                                                            item.score_obtained
                                                                                        )
                                                                                    }

                                                                                    {" / "}

                                                                                    {
                                                                                        formatNumber(
                                                                                            item.total_marks
                                                                                        )
                                                                                    }

                                                                                </strong>

                                                                            </td>


                                                                            <td>

                                                                                <span
                                                                                    className={
                                                                                        "leaderboard-percentage"
                                                                                    }
                                                                                >

                                                                                    {
                                                                                        formatNumber(
                                                                                            item.percentage
                                                                                        )
                                                                                    }%

                                                                                </span>

                                                                            </td>

                                                                        </tr>
                                                                    )
                                                                )
                                                            }

                                                        </tbody>

                                                    </table>

                                                </div>
                                            )
                                    }

                                </section>

                            </>
                        )
            }

        </section>
    );
}


export default QuizAnalytics;