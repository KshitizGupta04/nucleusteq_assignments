import {
    useEffect,
    useState
} from "react";

import {
    FaArrowRight,
    FaBook,
    FaCheckCircle,
    FaClipboardCheck,
    FaFolderOpen,
    FaTimesCircle
} from "react-icons/fa";

import {
    getCategories,
    getMyResults,
    getQuizzes
} from "../../services/studentService";

import {
    getMyProfile,
} from "../../services/authService";


function StudentOverview({
    onNavigate,
    onViewResult
}) {

    const [
        profile,
        setProfile
    ] = useState(null);


    const [
        categories,
        setCategories
    ] = useState([]);


    const [
        quizzes,
        setQuizzes
    ] = useState([]);


    const [
        results,
        setResults
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

            const loadOverview = async () => {

                try {

                    setLoading(true);

                    setError("");


                    const [
                        profileData,
                        categoryData,
                        quizData,
                        resultData
                    ] = await Promise.all([
                        getMyProfile(),
                        getCategories(),
                        getQuizzes(),
                        getMyResults()
                    ]);


                    setProfile(
                        profileData
                    );


                    setCategories(
                        Array.isArray(
                            categoryData
                        )
                            ? categoryData
                            : []
                    );


                    setQuizzes(
                        Array.isArray(
                            quizData
                        )
                            ? quizData
                            : []
                    );


                    setResults(
                        Array.isArray(
                            resultData
                        )
                            ? resultData
                            : []
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load dashboard."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadOverview();

        },
        []
    );


    const passedResults = results.filter(
        result =>
            result.status === "pass"
    ).length;


    const failedResults = results.filter(
        result =>
            result.status !== "pass"
    ).length;


    const recentResults = (
        results.slice(
            0,
            3
        )
    );


    const getResultStatusClass = (
        status
    ) => {

        return (
            status === "pass"
                ? "passed"
                : "failed"
        );
    };


    const formatStatus = (
        status
    ) => {

        return (
            status === "pass"
                ? "Passed"
                : "Failed"
        );
    };


    const getQuizTitle = (
        quizId
    ) => {

        const quiz = quizzes.find(
            item =>
                item.id === quizId
        );


        return (
            quiz?.title ||
            "Assessment"
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


        return numericScore.toFixed(
            2
        );
    };


    if (loading) {

        return (

            <div className="management-loading">

                Loading dashboard...

            </div>
        );
    }


    if (error) {

        return (

            <div className="error-message">

                {error}

            </div>
        );
    }


    return (

        <div className="student-overview">


            <section className="student-welcome-banner">

                <div>

                    <span className="student-welcome-label">

                        STUDENT DASHBOARD

                    </span>


                    <h2>

                        Welcome back
                        {
                            profile?.username
                                ? `, ${profile.username}!`
                                : "!"
                        }

                    </h2>


                    <p>
                        Explore assessments, test your
                        knowledge, and track your progress.
                    </p>

                </div>


                <button
                    type="button"
                    className="student-welcome-button"
                    onClick={
                        () =>
                            onNavigate(
                                "categories"
                            )
                    }
                >

                    Browse Categories

                    <FaArrowRight />

                </button>

            </section>


            <section className="student-overview-section">

                <div className="student-section-heading">

                    <div>

                        <h3>
                            Your Overview
                        </h3>

                        <p>
                            A quick summary of your
                            assessment activity.
                        </p>

                    </div>

                </div>


                <div className="student-stat-grid">


                    <article className="student-stat-card quizzes">

                        <div className="student-stat-icon">

                            <FaBook />

                        </div>


                        <div>

                            <strong>
                                {quizzes.length}
                            </strong>

                            <span>
                                Available Quizzes
                            </span>

                        </div>

                    </article>


                    <article className="student-stat-card completed">

                        <div className="student-stat-icon">

                            <FaClipboardCheck />

                        </div>


                        <div>

                            <strong>
                                {results.length}
                            </strong>

                            <span>
                                Completed Attempts
                            </span>

                        </div>

                    </article>


                    <article className="student-stat-card passed">

                        <div className="student-stat-icon">

                            <FaCheckCircle />

                        </div>


                        <div>

                            <strong>
                                {passedResults}
                            </strong>

                            <span>
                                Passed
                            </span>

                        </div>

                    </article>


                    <article className="student-stat-card failed">

                        <div className="student-stat-icon">

                            <FaTimesCircle />

                        </div>


                        <div>

                            <strong>
                                {failedResults}
                            </strong>

                            <span>
                                Failed
                            </span>

                        </div>

                    </article>

                </div>

            </section>


            <section className="student-overview-section">

                <div className="student-section-heading">

                    <div>

                        <h3>
                            Explore Assessments
                        </h3>

                        <p>
                            Choose where you want to
                            continue.
                        </p>

                    </div>

                </div>


                <div className="student-action-grid">


                    <article className="student-action-card">

                        <div className="student-action-icon">

                            <FaFolderOpen />

                        </div>


                        <div className="student-action-content">

                            <h4>
                                Categories
                            </h4>

                            <p>
                                Browse {
                                    categories.length
                                } available assessment {
                                    categories.length === 1
                                        ? "category"
                                        : "categories"
                                }.
                            </p>

                        </div>


                        <button
                            type="button"
                            onClick={
                                () =>
                                    onNavigate(
                                        "categories"
                                    )
                            }
                        >

                            Explore Categories

                            <FaArrowRight />

                        </button>

                    </article>


                    <article className="student-action-card">

                        <div className="student-action-icon">

                            <FaBook />

                        </div>


                        <div className="student-action-content">

                            <h4>
                                Available Quizzes
                            </h4>

                            <p>
                                You currently have {
                                    quizzes.length
                                } {
                                    quizzes.length === 1
                                        ? "quiz"
                                        : "quizzes"
                                } available to explore.
                            </p>

                        </div>


                        <button
                            type="button"
                            onClick={
                                () =>
                                    onNavigate(
                                        "categories"
                                    )
                            }
                        >

                            View Quizzes

                            <FaArrowRight />

                        </button>

                    </article>


                    <article className="student-action-card">

                        <div className="student-action-icon">

                            <FaClipboardCheck />

                        </div>


                        <div className="student-action-content">

                            <h4>
                                My Results
                            </h4>

                            <p>
                                Review your completed
                                assessments and detailed
                                performance.
                            </p>

                        </div>


                        <button
                            type="button"
                            onClick={
                                () =>
                                    onNavigate(
                                        "results"
                                    )
                            }
                        >

                            View Results

                            <FaArrowRight />

                        </button>

                    </article>

                </div>

            </section>


            <section className="student-overview-section">

                <div className="student-section-heading">

                    <div>

                        <h3>
                            Recent Performance
                        </h3>

                        <p>
                            Your latest completed
                            assessment results.
                        </p>

                    </div>


                    {
                        results.length > 3 && (

                            <button
                                type="button"
                                className={
                                    "student-view-all-button"
                                }
                                onClick={
                                    () =>
                                        onNavigate(
                                            "results"
                                        )
                                }
                            >

                                View All Results

                                <FaArrowRight />

                            </button>
                        )
                    }

                </div>


                {
                    recentResults.length === 0
                        ? (

                            <div className="student-recent-empty">

                                <FaClipboardCheck />

                                <h4>
                                    No results yet
                                </h4>

                                <p>
                                    Complete your first
                                    quiz to see your
                                    performance here.
                                </p>

                            </div>
                        )
                        : (

                            <div className="student-recent-results">

                                {
                                    recentResults.map(
                                        result => (

                                            <article
                                                key={
                                                    result.result_id
                                                }
                                                className={
                                                    "student-recent-result"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "student-recent-result-main"
                                                    }
                                                >

                                                    <div
                                                        className={
                                                            "student-recent-result-icon"
                                                        }
                                                    >

                                                        <FaClipboardCheck />

                                                    </div>


                                                    <div>

                                                        <h4>
                                                            {
                                                                getQuizTitle(
                                                                    result.quiz_id
                                                                )
                                                            }
                                                        </h4>


                                                        <p>
                                                            Score: {
                                                                formatScore(
                                                                    result.score_obtained
                                                                )
                                                            } / {
                                                                result.total_marks
                                                            }
                                                        </p>

                                                    </div>

                                                </div>


                                                <div
                                                    className={
                                                        "student-recent-result-actions"
                                                    }
                                                >

                                                    <span
                                                        className={
                                                            "student-result-status " +
                                                            getResultStatusClass(
                                                                result.status
                                                            )
                                                        }
                                                    >

                                                        {
                                                            formatStatus(
                                                                result.status
                                                            )
                                                        }

                                                    </span>


                                                    <button
                                                        type="button"
                                                        onClick={
                                                            () =>
                                                                onViewResult(
                                                                    result.result_id
                                                                )
                                                        }
                                                    >

                                                        View Result

                                                        <FaArrowRight />

                                                    </button>

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


export default StudentOverview;