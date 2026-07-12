import {
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import {
    FaBars,
    FaBook,
    FaChartBar,
    FaClipboardCheck,
    FaHome,
    FaSignOutAlt,
    FaTimes
} from "react-icons/fa";

import AvailableQuizzes from "./AvailableQuizzes";
import MyResults from "./MyResults";
import QuizAttempt from "./QuizAttempt";
import ResultBreakdown from "./ResultBreakdown";


const ACTIVE_ATTEMPT_KEY = (
    "active_attempt_id"
);


const getStoredAttemptId = () => {

    return sessionStorage.getItem(
        ACTIVE_ATTEMPT_KEY
    );
};


const SIDEBAR_ITEMS = [
    {
        id: "dashboard",
        label: "Dashboard",
        title: "Student Dashboard",
        icon: FaHome
    },
    {
        id: "quizzes",
        label: "Available Quizzes",
        title: "Available Quizzes",
        icon: FaBook
    },
    {
        id: "results",
        label: "My Results",
        title: "My Results",
        icon: FaChartBar
    }
];


function StudentDashboard() {

    const navigate = useNavigate();


    const [
        activeAttemptId,
        setActiveAttemptId
    ] = useState(
        getStoredAttemptId
    );


    const [
        activeSection,
        setActiveSection
    ] = useState(
        () => {

            return getStoredAttemptId()
                ? "attempt"
                : "dashboard";
        }
    );


    const [
        sidebarOpen,
        setSidebarOpen
    ] = useState(false);


    const [
        selectedResultId,
        setSelectedResultId
    ] = useState(null);


    const handleLogout = () => {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "refresh_token"
        );

        localStorage.removeItem(
            "role"
        );

        sessionStorage.removeItem(
            ACTIVE_ATTEMPT_KEY
        );

        navigate(
            "/login",
            {
                replace: true
            }
        );
    };


    const handleSectionChange = (
        section
    ) => {

        setActiveSection(
            section
        );

        setSelectedResultId(
            null
        );

        setSidebarOpen(
            false
        );
    };


    const handleStartAttempt = (
        attemptId
    ) => {

        sessionStorage.setItem(
            ACTIVE_ATTEMPT_KEY,
            attemptId
        );

        setActiveAttemptId(
            attemptId
        );

        setActiveSection(
            "attempt"
        );
    };


    const handleAttemptSubmitted = () => {

        sessionStorage.removeItem(
            ACTIVE_ATTEMPT_KEY
        );

        setActiveAttemptId(
            null
        );

        setActiveSection(
            "results"
        );
    };


    const handleViewResult = (
        resultId
    ) => {

        setSelectedResultId(
            resultId
        );

        setActiveSection(
            "result-breakdown"
        );
    };


    const getSectionTitle = () => {

        if (
            activeSection === "attempt"
        ) {

            return "Quiz Attempt";
        }

        if (
            activeSection ===
            "result-breakdown"
        ) {

            return "Result Breakdown";
        }

        const currentItem = (
            SIDEBAR_ITEMS.find(
                item =>
                    item.id ===
                    activeSection
            )
        );

        return (
            currentItem?.title ||
            "Student Dashboard"
        );
    };


    const renderDashboardOverview = () => {

        return (

            <div className="dashboard-welcome">

                <FaClipboardCheck
                    className="dashboard-welcome-icon"
                />

                <h2>
                    Welcome to the Assessment Portal
                </h2>

                <p>
                    Choose an available quiz,
                    complete your assessment,
                    and view your results.
                </p>

                <button
                    type="button"
                    className="primary-button"
                    onClick={
                        () =>
                            handleSectionChange(
                                "quizzes"
                            )
                    }
                >
                    View Available Quizzes
                </button>

            </div>
        );
    };


    const renderSectionContent = () => {

        switch (
            activeSection
        ) {

            case "quizzes":

                return (

                    <AvailableQuizzes
                        onStartAttempt={
                            handleStartAttempt
                        }
                    />
                );


            case "attempt":

                if (!activeAttemptId) {

                    return (
                        renderDashboardOverview()
                    );
                }

                return (

                    <QuizAttempt
                        attemptId={
                            activeAttemptId
                        }
                        onSubmitted={
                            handleAttemptSubmitted
                        }
                    />
                );


            case "results":

                return (

                    <MyResults
                        onViewResult={
                            handleViewResult
                        }
                    />
                );


            case "result-breakdown":

                return (

                    <ResultBreakdown
                        resultId={
                            selectedResultId
                        }
                        onBack={
                            () => {

                                setSelectedResultId(
                                    null
                                );

                                setActiveSection(
                                    "results"
                                );
                            }
                        }
                    />
                );


            case "dashboard":
            default:

                return (
                    renderDashboardOverview()
                );
        }
    };


    return (

        <div className="dashboard-layout">

            <aside
                className={
                    sidebarOpen
                        ? (
                            "dashboard-sidebar " +
                            "sidebar-open"
                        )
                        : "dashboard-sidebar"
                }
            >

                <div className="sidebar-header">

                    <h2>
                        Assessment Portal
                    </h2>

                    <button
                        type="button"
                        className="sidebar-close-button"
                        onClick={
                            () =>
                                setSidebarOpen(
                                    false
                                )
                        }
                        aria-label="Close sidebar"
                    >
                        <FaTimes />
                    </button>

                </div>


                <nav className="sidebar-navigation">

                    {
                        SIDEBAR_ITEMS.map(
                            item => {

                                const Icon = (
                                    item.icon
                                );

                                const isActive = (
                                    activeSection ===
                                    item.id
                                );

                                return (

                                    <button
                                        key={item.id}
                                        type="button"
                                        className={
                                            isActive
                                                ? (
                                                    "sidebar-link " +
                                                    "active"
                                                )
                                                : "sidebar-link"
                                        }
                                        onClick={
                                            () =>
                                                handleSectionChange(
                                                    item.id
                                                )
                                        }
                                    >

                                        <Icon />

                                        <span>
                                            {item.label}
                                        </span>

                                    </button>
                                );
                            }
                        )
                    }

                </nav>


                <button
                    type="button"
                    className="sidebar-logout-button"
                    onClick={
                        handleLogout
                    }
                >

                    <FaSignOutAlt />

                    <span>
                        Logout
                    </span>

                </button>

            </aside>


            {
                sidebarOpen && (

                    <div
                        className="sidebar-overlay"
                        onClick={
                            () =>
                                setSidebarOpen(
                                    false
                                )
                        }
                    />

                )
            }


            <main className="dashboard-main">

                <header className="dashboard-topbar">

                    <button
                        type="button"
                        className="menu-button"
                        onClick={
                            () =>
                                setSidebarOpen(
                                    true
                                )
                        }
                        aria-label="Open sidebar"
                    >
                        <FaBars />
                    </button>


                    <div>

                        <h1>
                            {getSectionTitle()}
                        </h1>

                        <p>
                            Take assessments and
                            track your performance
                        </p>

                    </div>

                </header>


                <section className="dashboard-content">

                    {
                        renderSectionContent()
                    }

                </section>

            </main>

        </div>
    );
}


export default StudentDashboard;