import {
    useCallback,
    useEffect,
    useRef,
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import {
    FaBars
} from "react-icons/fa";

import {
    submitAttempt
} from "../../services/studentService";

import {
    logoutUser
} from "../../utils/logout";

import {
    STUDENT_SIDEBAR_ITEMS
} from "../../constants/studentSidebar";

import AvailableQuizzes from "./AvailableQuizzes";
import MyProfile from "../../components/MyProfile";
import MyResults from "./MyResults";
import QuizAttempt from "./QuizAttempt";
import ResultBreakdown from "./ResultBreakdown";
import StudentCategories from "./StudentCategories";
import StudentOverview from "./StudentOverview";
import StudentSidebar from "./StudentSidebar";


const ATTEMPT_GRACE_PERIOD_MS = 20000;


function StudentDashboard() {

    const navigate = useNavigate();


    const [
        activeSection,
        setActiveSection
    ] = useState("dashboard");


    const [
        sidebarOpen,
        setSidebarOpen
    ] = useState(false);


    const [
        selectedCategory,
        setSelectedCategory
    ] = useState(null);


    const [
        currentAttemptId,
        setCurrentAttemptId
    ] = useState(null);


    const [
        currentAttemptQuizId,
        setCurrentAttemptQuizId
    ] = useState(null);


    const [
        pendingAttemptId,
        setPendingAttemptId
    ] = useState(null);


    const [
        pendingAttemptQuizId,
        setPendingAttemptQuizId
    ] = useState(null);


    const [
        selectedResultId,
        setSelectedResultId
    ] = useState(null);


    const [
        attemptNotice,
        setAttemptNotice
    ] = useState("");


    const graceTimerRef = useRef(null);

    const graceStartedAtRef = useRef(null);

    const autoSubmittingRef = useRef(false);


    const clearGraceTimer = useCallback(
        () => {

            if (
                graceTimerRef.current
            ) {

                clearTimeout(
                    graceTimerRef.current
                );

                graceTimerRef.current = null;
            }


            graceStartedAtRef.current = null;

        },
        []
    );


    const clearActiveAttempt = useCallback(
        () => {

            clearGraceTimer();


            setCurrentAttemptId(
                null
            );

            setCurrentAttemptQuizId(
                null
            );

            setPendingAttemptId(
                null
            );

            setPendingAttemptQuizId(
                null
            );


            autoSubmittingRef.current = false;

        },
        [
            clearGraceTimer
        ]
    );


    const autoSubmitPendingAttempt = useCallback(
        async (
            attemptId
        ) => {

            if (
                !attemptId ||
                autoSubmittingRef.current
            ) {

                return;
            }


            autoSubmittingRef.current = true;


            try {

                await submitAttempt(
                    attemptId,
                    {}
                );


                clearActiveAttempt();


                setAttemptNotice(
                    "Your quiz was automatically " +
                    "submitted because you did not " +
                    "resume it within 20 seconds."
                );


                setActiveSection(
                    "results"
                );

            } catch (err) {

                const message = (
                    err.message ||
                    "Failed to automatically submit quiz."
                );


                if (
                    message
                        .toLowerCase()
                        .includes(
                            "already submitted"
                        )
                ) {

                    clearActiveAttempt();


                    setAttemptNotice(
                        "Your quiz has already been submitted."
                    );


                    setActiveSection(
                        "results"
                    );


                    return;
                }


                setAttemptNotice(
                    message
                );


                autoSubmittingRef.current = false;
            }

        },
        [
            clearActiveAttempt
        ]
    );


    const startGracePeriod = useCallback(
        (
            attemptId,
            quizId
        ) => {

            if (!attemptId) {

                return;
            }


            clearGraceTimer();


            setPendingAttemptId(
                attemptId
            );

            setPendingAttemptQuizId(
                quizId
            );


            graceStartedAtRef.current = (
                Date.now()
            );


            graceTimerRef.current = setTimeout(
                () => {

                    autoSubmitPendingAttempt(
                        attemptId
                    );

                },
                ATTEMPT_GRACE_PERIOD_MS
            );

        },
        [
            autoSubmitPendingAttempt,
            clearGraceTimer
        ]
    );


    const handleLeaveAttempt = useCallback(
        (
            nextSection
        ) => {

            if (
                currentAttemptId
            ) {

                startGracePeriod(
                    currentAttemptId,
                    currentAttemptQuizId
                );


                setCurrentAttemptId(
                    null
                );

                setCurrentAttemptQuizId(
                    null
                );


                setAttemptNotice(
                    "You have 20 seconds to resume " +
                    "your active quiz. After that, " +
                    "it will be automatically submitted."
                );
            }


            setActiveSection(
                "results"
            );


            setSidebarOpen(
                false
            );

        },
        [
            currentAttemptId,
            currentAttemptQuizId,
            startGracePeriod
        ]
    );


    const handleSectionChange = (
        section
    ) => {

        if (
            activeSection === "attempt" &&
            currentAttemptId
        ) {

            handleLeaveAttempt(
                section
            );

            return;
        }


        setActiveSection(
            section
        );


        setSidebarOpen(
            false
        );
    };


    const handleViewQuizzes = (
        category
    ) => {

        setSelectedCategory(
            category
        );


        if (
            activeSection === "attempt" &&
            currentAttemptId
        ) {

            handleLeaveAttempt(
                "quizzes"
            );

            return;
        }


        setActiveSection(
            "quizzes"
        );
    };


    const handleBackToCategories = () => {

        setSelectedCategory(
            null
        );


        setActiveSection(
            "categories"
        );
    };


    const handleStartAttempt = (
        attemptId,
        resumed = false,
        quizId = null
    ) => {

        clearGraceTimer();


        setPendingAttemptId(
            null
        );

        setPendingAttemptQuizId(
            null
        );


        setCurrentAttemptId(
            attemptId
        );

        setCurrentAttemptQuizId(
            quizId
        );


        setAttemptNotice(
            resumed
                ? "Your active quiz has been resumed."
                : ""
        );


        autoSubmittingRef.current = false;


        setActiveSection(
            "attempt"
        );
    };


    const handleResumeAttempt = (
        attemptId,
        quizId
    ) => {

        if (
            !attemptId
        ) {

            return;
        }


        clearGraceTimer();


        setPendingAttemptId(
            null
        );

        setPendingAttemptQuizId(
            null
        );


        setCurrentAttemptId(
            attemptId
        );

        setCurrentAttemptQuizId(
            quizId
        );


        setAttemptNotice(
            "Your active quiz has been resumed."
        );


        autoSubmittingRef.current = false;


        setActiveSection(
            "attempt"
        );
    };


    const handleAttemptComplete = () => {

        clearActiveAttempt();


        setAttemptNotice(
            ""
        );


        setActiveSection(
            "results"
        );
    };


    const handleViewResult = (
        resultId
    ) => {

        if (!resultId) {

            setAttemptNotice(
                "Result ID is missing."
            );

            return;
        }


        setSelectedResultId(
            resultId
        );


        setActiveSection(
            "result-details"
        );
    };


    const handleBackToResults = () => {

        setSelectedResultId(
            null
        );


        setActiveSection(
            "results"
        );
    };


    const handleLogout = async () => {

        if (
            currentAttemptId
        ) {

            try {

                await submitAttempt(
                    currentAttemptId,
                    {}
                );

            } catch (err) {

                const message = (
                    err.message || ""
                ).toLowerCase();


                if (
                    !message.includes(
                        "already submitted"
                    )
                ) {

                    setAttemptNotice(
                        err.message ||
                        "Failed to submit active quiz."
                    );

                    return;
                }
            }
        }


        if (
            pendingAttemptId
        ) {

            try {

                await submitAttempt(
                    pendingAttemptId,
                    {}
                );

            } catch (err) {

                const message = (
                    err.message || ""
                ).toLowerCase();


                if (
                    !message.includes(
                        "already submitted"
                    )
                ) {

                    setAttemptNotice(
                        err.message ||
                        "Failed to submit active quiz."
                    );

                    return;
                }
            }
        }


        clearActiveAttempt();


        logoutUser(
            navigate
        );
    };


    useEffect(
        () => {

            if (
                !pendingAttemptId ||
                !graceStartedAtRef.current
            ) {

                return;
            }


            const handleVisibilityChange = () => {

                if (
                    document.hidden
                ) {

                    return;
                }


                const elapsedTime = (
                    Date.now() -
                    graceStartedAtRef.current
                );


                if (
                    elapsedTime >=
                    ATTEMPT_GRACE_PERIOD_MS
                ) {

                    autoSubmitPendingAttempt(
                        pendingAttemptId
                    );
                }
            };


            document.addEventListener(
                "visibilitychange",
                handleVisibilityChange
            );


            return () => {

                document.removeEventListener(
                    "visibilitychange",
                    handleVisibilityChange
                );
            };

        },
        [
            pendingAttemptId,
            autoSubmitPendingAttempt
        ]
    );


    useEffect(
        () => {

            return () => {

                if (
                    graceTimerRef.current
                ) {

                    clearTimeout(
                        graceTimerRef.current
                    );
                }
            };

        },
        []
    );


    const getSectionTitle = () => {

        if (
            activeSection === "quizzes"
        ) {

            return (
                selectedCategory?.name ||
                "Available Quizzes"
            );
        }


        if (
            activeSection === "attempt"
        ) {

            return "Quiz Attempt";
        }


        if (
            activeSection === "result-details"
        ) {

            return "Result Details";
        }


        const currentItem = (
            STUDENT_SIDEBAR_ITEMS.find(
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


    const renderSectionContent = () => {

        switch (
            activeSection
        ) {

            case "dashboard":

                return (

                    <StudentOverview
                        onNavigate={
                            handleSectionChange
                        }
                        onViewResult={
                            handleViewResult
                        }
                    />
                );


            case "categories":

                return (

                    <StudentCategories
                        onViewQuizzes={
                            handleViewQuizzes
                        }
                    />
                );


            case "quizzes":

                return (

                    <AvailableQuizzes
                        selectedCategory={
                            selectedCategory
                        }
                        onBackToCategories={
                            handleBackToCategories
                        }
                        onStartAttempt={
                            handleStartAttempt
                        }
                        onResumeAttempt={
                            handleResumeAttempt
                        }
                        pendingAttemptId={
                            pendingAttemptId
                        }
                        pendingAttemptQuizId={
                            pendingAttemptQuizId
                        }
                    />
                );


            case "attempt":

                return (

                    <QuizAttempt
                        attemptId={
                            currentAttemptId
                        }
                        onSubmitted={
                            handleAttemptComplete
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


            case "result-details":

                return (

                    <ResultBreakdown
                        resultId={
                            selectedResultId
                        }
                        onBack={
                            handleBackToResults
                        }
                    />
                );


            case "profile":

                return (

                    <MyProfile />
                );


            default:

                return null;
        }
    };


    return (

        <div className="dashboard-layout">

            <StudentSidebar
                activeSection={
                    activeSection
                }
                sidebarOpen={
                    sidebarOpen
                }
                onClose={
                    () =>
                        setSidebarOpen(
                            false
                        )
                }
                onSectionChange={
                    handleSectionChange
                }
                onLogout={
                    handleLogout
                }
            />


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
                            {
                                getSectionTitle()
                            }
                        </h1>

                        <p>
                            Explore assessments and
                            track your progress
                        </p>

                    </div>

                </header>


                <section className="dashboard-content">

                    {
                        attemptNotice && (

                            <div
                                className={
                                    "success-message"
                                }
                            >

                                {attemptNotice}

                            </div>
                        )
                    }


                    {
                        renderSectionContent()
                    }

                </section>

            </main>

        </div>
    );
}


export default StudentDashboard;