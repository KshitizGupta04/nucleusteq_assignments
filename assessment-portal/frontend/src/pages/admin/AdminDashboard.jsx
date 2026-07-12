import {
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import {
    FaBars,
    FaBook,
    FaClipboardCheck,
    FaFolderOpen,
    FaQuestionCircle,
    FaSignOutAlt,
    FaTimes
} from "react-icons/fa";

import AdminOverview from "./AdminOverview";
import AdminResults from "./AdminResults";
import CategoryManagement from "./CategoryManagement";
import QuestionManagement from "./QuestionManagement";
import QuizManagement from "./QuizManagement";


const SIDEBAR_ITEMS = [
    {
        id: "dashboard",
        label: "Dashboard",
        title: "Dashboard Overview",
        icon: FaClipboardCheck
    },
    {
        id: "categories",
        label: "Categories",
        title: "Category Management",
        icon: FaFolderOpen
    },
    {
        id: "quizzes",
        label: "Quizzes",
        title: "Quiz Management",
        icon: FaBook
    },
    {
        id: "questions",
        label: "Questions",
        title: "Question Management",
        icon: FaQuestionCircle
    },
    {
        id: "results",
        label: "Results",
        title: "Student Results",
        icon: FaClipboardCheck
    }
];


function AdminDashboard() {

    const navigate = useNavigate();

    const [
        activeSection,
        setActiveSection
    ] = useState("dashboard");

    const [
        sidebarOpen,
        setSidebarOpen
    ] = useState(false);


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

        setSidebarOpen(
            false
        );
    };


    const getSectionTitle = () => {

        const currentItem = SIDEBAR_ITEMS.find(
            item => item.id === activeSection
        );

        return (
            currentItem?.title ||
            "Dashboard Overview"
        );
    };


    const renderSectionContent = () => {

        const managementComponents = {
            dashboard: (
                <AdminOverview
                    onNavigate={
                        handleSectionChange
                    }
                />
            ),

            categories: (
                <CategoryManagement />
            ),

            quizzes: (
                <QuizManagement />
            ),

            questions: (
                <QuestionManagement />
            ),

            results: (
                <AdminResults />
            )
        };


        return (
            managementComponents[
                activeSection
            ] || null
        );
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
                    onClick={handleLogout}
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
                            Manage your assessment portal
                        </p>

                    </div>

                </header>


                <section className="dashboard-content">

                    {renderSectionContent()}

                </section>

            </main>

        </div>
    );
}


export default AdminDashboard;