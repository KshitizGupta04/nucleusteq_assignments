import {
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import {
    FaBars
} from "react-icons/fa";

import MyProfile from "../../components/MyProfile";
import ProfileMenu from "../../components/ProfileMenu";

import {
    ADMIN_SIDEBAR_ITEMS
} from "../../constants/adminSidebar";

import {
    logoutUser
} from "../../utils/logout";

import AdminOverview from "./AdminOverview";
import AdminResults from "./AdminResults";
import AdminSidebar from "./AdminSidebar";
import CategoryManagement from "./CategoryManagement";
import QuestionManagement from "./QuestionManagement";
import QuizAnalytics from "./QuizAnalytics";
import QuizManagement from "./QuizManagement";


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

        logoutUser(
            navigate
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


    const handleViewProfile = () => {

        setActiveSection(
            "profile"
        );

        setSidebarOpen(
            false
        );
    };


    const getSectionTitle = () => {

        if (
            activeSection === "profile"
        ) {

            return "My Profile";
        }


        const currentItem = (
            ADMIN_SIDEBAR_ITEMS.find(
                item =>
                    item.id ===
                    activeSection
            )
        );


        return (
            currentItem?.title ||
            "Dashboard Overview"
        );
    };


    const getSectionDescription = () => {

        if (
            activeSection === "profile"
        ) {

            return (
                "View your account information"
            );
        }


        return (
            "Manage your assessment portal"
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
            ),

            analytics: (
                <QuizAnalytics />
            ),

            profile: (
                <MyProfile />
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

            <AdminSidebar
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


                    <div className="dashboard-topbar-content">

                        <div
                            className={
                                "dashboard-topbar-title"
                            }
                        >

                            <h1>
                                {
                                    getSectionTitle()
                                }
                            </h1>

                            <p>
                                {
                                    getSectionDescription()
                                }
                            </p>

                        </div>


                        <div
                            className={
                                "dashboard-topbar-actions"
                            }
                        >

                            <ProfileMenu
                                onViewProfile={
                                    handleViewProfile
                                }
                            />

                        </div>

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


export default AdminDashboard;