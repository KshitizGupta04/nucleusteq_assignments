const API_ENDPOINTS = {

    AUTH: {
        LOGIN: "/auth/login",
        REGISTER: "/auth/register",
        REFRESH: "/auth/refresh",
        PROFILE: "/auth/me"
    },

    CATEGORIES: {
        BASE: "/categories/",

        BY_ID: (
            categoryId
        ) => (
            `/categories/${categoryId}`
        )
    },

    QUIZZES: {
        BASE: "/quizzes/",

        BY_ID: (
            quizId
        ) => (
            `/quizzes/${quizId}`
        )
    },

    QUESTIONS: {
        BASE: "/questions/",

        BY_ID: (
            questionId
        ) => (
            `/questions/${questionId}`
        ),

        ADMIN_BY_QUIZ: (
            quizId
        ) => (
            `/questions/admin/quiz/${quizId}`
        ),

        BY_QUIZ: (
            quizId
        ) => (
            `/questions/quiz/${quizId}`
        )
    },

    ATTEMPTS: {
        START: "/attempts/start",

        ANSWER: (
            attemptId
        ) => (
            `/attempts/${attemptId}/answer`
        ),

        BY_ID: (
            attemptId
        ) => (
            `/attempts/${attemptId}`
        ),

        SUBMIT: (
            attemptId
        ) => (
            `/attempts/${attemptId}/submit`
        )
    },

    RESULTS: {
        MY_RESULTS: "/results/me",

        BY_ID: (
            resultId
        ) => (
            `/results/${resultId}`
        ),

        BREAKDOWN: (
            resultId
        ) => (
            `/results/${resultId}/breakdown`
        ),

        ADMIN_DASHBOARD: (
            "/results/admin/dashboard"
        ),

        QUIZ_STATISTICS: (
            quizId
        ) => (
            `/results/admin/quiz/${quizId}/statistics`
        ),

        QUIZ_LEADERBOARD: (
            quizId
        ) => (
            `/results/admin/quiz/${quizId}/leaderboard`
        )
    }
};


export default API_ENDPOINTS;