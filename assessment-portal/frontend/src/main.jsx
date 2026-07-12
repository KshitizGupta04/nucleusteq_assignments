import {
    createRoot
} from "react-dom/client";


import "./styles/global.css";
import "./styles/auth.css";

import "./styles/admin/adminLayout.css";
import "./styles/admin/adminCommon.css";
import "./styles/admin/categoryManagement.css";
import "./styles/admin/quizManagement.css";
import "./styles/admin/questionManagement.css";
import "./styles/admin/adminOverview.css";
import "./styles/admin/adminResults.css";

import "./styles/student/student.css";
import "./styles/student/quizAttempt.css";
import "./styles/student/resultBreakdown.css";



import App from "./App.jsx";


createRoot(
    document.getElementById(
        "root"
    )
).render(

    <App />

);