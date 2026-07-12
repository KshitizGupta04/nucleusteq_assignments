import {
    useEffect,
    useState
} from "react";

import {
    FaBook,
    FaClipboardCheck,
    FaFolderOpen,
    FaQuestionCircle
} from "react-icons/fa";

import {
    getAdminQuestionsByQuiz,
    getAdminResults,
    getCategories,
    getQuizzes
} from "../../services/api";


function AdminOverview({
    onNavigate
}) {

    const [
        stats,
        setStats
    ] = useState({
        categories: 0,
        quizzes: 0,
        questions: 0,
        results: 0
    });

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

            const loadDashboardStats = async () => {

                setLoading(true);

                setError("");

                try {

                    const [
                        categories,
                        quizzes,
                        results
                    ] = await Promise.all([
                        getCategories(),
                        getQuizzes(),
                        getAdminResults()
                    ]);


                    const safeCategories = (
                        Array.isArray(categories)
                            ? categories
                            : []
                    );

                    const safeQuizzes = (
                        Array.isArray(quizzes)
                            ? quizzes
                            : []
                    );

                    const safeResults = (
                        Array.isArray(results)
                            ? results
                            : []
                    );


                    const questionResponses = (
                        await Promise.all(
                            safeQuizzes.map(
                                quiz =>
                                    getAdminQuestionsByQuiz(
                                        quiz.id
                                    )
                            )
                        )
                    );


                    const totalQuestions = (
                        questionResponses.reduce(
                            (
                                total,
                                questions
                            ) => {

                                return (
                                    total +
                                    (
                                        Array.isArray(
                                            questions
                                        )
                                            ? questions.length
                                            : 0
                                    )
                                );
                            },
                            0
                        )
                    );


                    setStats({
                        categories:
                            safeCategories.length,

                        quizzes:
                            safeQuizzes.length,

                        questions:
                            totalQuestions,

                        results:
                            safeResults.length
                    });

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load dashboard statistics."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadDashboardStats();

        },
        []
    );


    const statCards = [
        {
            id: "categories",
            title: "Categories",
            value: stats.categories,
            description:
                "Assessment categories available",
            icon: FaFolderOpen
        },
        {
            id: "quizzes",
            title: "Quizzes",
            value: stats.quizzes,
            description:
                "Quizzes currently available",
            icon: FaBook
        },
        {
            id: "questions",
            title: "Questions",
            value: stats.questions,
            description:
                "Questions across all quizzes",
            icon: FaQuestionCircle
        },
        {
            id: "results",
            title: "Results",
            value: stats.results,
            description:
                "Student assessment results",
            icon: FaClipboardCheck
        }
    ];


    if (loading) {

        return (

            <div className="admin-overview-loading">

                Loading dashboard overview...

            </div>
        );
    }


    return (

        <div className="admin-overview">

            <section className="admin-welcome-card">

                <div>

                    <span className="admin-welcome-label">
                        ADMIN PANEL
                    </span>

                    <h2>
                        Welcome to the Assessment Portal
                    </h2>

                    <p>
                        Manage categories, quizzes,
                        questions, and review student
                        assessment results from one place.
                    </p>

                </div>

            </section>


            {
                error && (

                    <div className="admin-overview-error">

                        {error}

                    </div>
                )
            }


            <section className="admin-stats-grid">

                {
                    statCards.map(
                        card => {

                            const Icon = card.icon;

                            return (

                                <button
                                    key={card.id}
                                    type="button"
                                    className={
                                        "admin-stat-card " +
                                        `admin-stat-${card.id}`
                                    }
                                    onClick={
                                        () =>
                                            onNavigate(
                                                card.id
                                            )
                                    }
                                >

                                    <div className="admin-stat-icon">

                                        <Icon />

                                    </div>


                                    <div className="admin-stat-content">

                                        <span className="admin-stat-title">
                                            {card.title}
                                        </span>

                                        <strong className="admin-stat-value">
                                            {card.value}
                                        </strong>

                                        <p>
                                            {card.description}
                                        </p>

                                    </div>

                                </button>
                            );
                        }
                    )
                }

            </section>

        </div>
    );
}


export default AdminOverview;