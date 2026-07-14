import {
    FaSignOutAlt,
    FaTimes
} from "react-icons/fa";

import {
    STUDENT_SIDEBAR_ITEMS
} from "../../constants/studentSidebar";


function StudentSidebar({
    activeSection,
    sidebarOpen,
    onClose,
    onSectionChange,
    onLogout
}) {

    return (

        <>

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
                        className={
                            "sidebar-close-button"
                        }
                        onClick={
                            onClose
                        }
                        aria-label="Close sidebar"
                    >

                        <FaTimes />

                    </button>

                </div>


                <nav className="sidebar-navigation">

                    {
                        STUDENT_SIDEBAR_ITEMS.map(
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
                                        key={
                                            item.id
                                        }
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
                                                onSectionChange(
                                                    item.id
                                                )
                                        }
                                    >

                                        <Icon />

                                        <span>
                                            {
                                                item.label
                                            }
                                        </span>

                                    </button>
                                );
                            }
                        )
                    }

                </nav>


                <button
                    type="button"
                    className={
                        "sidebar-logout-button"
                    }
                    onClick={
                        onLogout
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
                        className={
                            "sidebar-overlay"
                        }
                        onClick={
                            onClose
                        }
                    />

                )
            }

        </>
    );
}


export default StudentSidebar;