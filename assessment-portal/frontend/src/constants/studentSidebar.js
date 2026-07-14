import {
    FaClipboardCheck,
    FaFolderOpen,
    FaHome,
    FaUser
} from "react-icons/fa";


export const STUDENT_SIDEBAR_ITEMS = [
    {
        id: "dashboard",
        label: "Dashboard",
        title: "Student Dashboard",
        icon: FaHome
    },
    {
        id: "categories",
        label: "Categories",
        title: "Assessment Categories",
        icon: FaFolderOpen
    },
    {
        id: "results",
        label: "My Results",
        title: "My Results",
        icon: FaClipboardCheck
    },
    {
        id: "profile",
        label: "My Profile",
        title: "My Profile",
        icon: FaUser
    }
];