import {
    FaBook,
    FaChartBar,
    FaClipboardCheck,
    FaFolderOpen,
    FaQuestionCircle
} from "react-icons/fa";


export const ADMIN_SIDEBAR_ITEMS = [
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
    },
    {
        id: "analytics",
        label: "Quiz Analytics",
        title: "Quiz Analytics",
        icon: FaChartBar
    }
];