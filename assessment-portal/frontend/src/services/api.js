import {
    encryptPassword
} from "../utils/passwordEncryption";


const API_BASE_URL = (
    "http://127.0.0.1:8000/api/v1"
);


export const apiRequest = async (
    endpoint,
    options = {}
) => {

    const token = localStorage.getItem(
        "access_token"
    );

    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };

    if (token) {

        headers.Authorization = (
            `Bearer ${token}`
        );
    }

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers
        }
    );

    let data;

    try {

        data = await response.json();

    } catch {

        data = {};
    }

    if (!response.ok) {

        let errorMessage = (
            "Something went wrong."
        );

        if (
            typeof data.detail === "string"
        ) {

            errorMessage = data.detail;

        } else if (
            Array.isArray(data.detail)
        ) {

            errorMessage = data.detail
                .map(
                    (error) => error.msg
                )
                .join(", ");

        } else if (
            data.detail &&
            typeof data.detail === "object"
        ) {

            errorMessage = (
                data.detail.message ||
                JSON.stringify(
                    data.detail
                )
            );
        }

        throw new Error(
            errorMessage
        );
    }

    return data;
};


export const loginUser = async (
    username,
    password
) => {

    const encryptedPassword = (
        await encryptPassword(
            password
        )
    );

    return apiRequest(
        "/auth/login",
        {
            method: "POST",

            body: JSON.stringify({
                username,
                password: encryptedPassword
            })
        }
    );
};


export const registerUser = async (
    username,
    email,
    password
) => {

    const encryptedPassword = (
        await encryptPassword(
            password
        )
    );

    return apiRequest(
        "/auth/register",
        {
            method: "POST",

            body: JSON.stringify({
                username,
                email,
                password: encryptedPassword
            })
        }
    );
};


export const getCategories = async () => {

    return apiRequest(
        "/categories/",
        {
            method: "GET"
        }
    );
};


export const getCategoryById = async (
    categoryId
) => {

    return apiRequest(
        `/categories/${categoryId}`,
        {
            method: "GET"
        }
    );
};


export const createCategory = async (
    name,
    description
) => {

    return apiRequest(
        "/categories/",
        {
            method: "POST",

            body: JSON.stringify({
                name,
                description
            })
        }
    );
};


export const updateCategory = async (
    categoryId,
    name,
    description
) => {

    return apiRequest(
        `/categories/${categoryId}`,
        {
            method: "PUT",

            body: JSON.stringify({
                name,
                description
            })
        }
    );
};


export const deleteCategory = async (
    categoryId
) => {

    return apiRequest(
        `/categories/${categoryId}`,
        {
            method: "DELETE"
        }
    );
};


export const getQuizzes = async () => {

    return apiRequest(
        "/quizzes/",
        {
            method: "GET"
        }
    );
};


export const createQuiz = async (
    quizData
) => {

    return apiRequest(
        "/quizzes/",
        {
            method: "POST",

            body: JSON.stringify(
                quizData
            )
        }
    );
};


export const updateQuiz = async (
    quizId,
    quizData
) => {

    return apiRequest(
        `/quizzes/${quizId}`,
        {
            method: "PUT",

            body: JSON.stringify(
                quizData
            )
        }
    );
};


export const deleteQuiz = async (
    quizId
) => {

    return apiRequest(
        `/quizzes/${quizId}`,
        {
            method: "DELETE"
        }
    );
};

export const getAdminQuestionsByQuiz = async (
    quizId
) => {

    return apiRequest(
        `/questions/admin/quiz/${quizId}`,
        {
            method: "GET"
        }
    );
};

export const getQuestionsByQuiz = async (
    quizId
) => {

    return apiRequest(
        `/questions/quiz/${quizId}`,
        {
            method: "GET"
        }
    );
};


export const createQuestion = async (
    questionData
) => {

    return apiRequest(
        "/questions/",
        {
            method: "POST",

            body: JSON.stringify(
                questionData
            )
        }
    );
};


export const updateQuestion = async (
    questionId,
    questionData
) => {

    return apiRequest(
        `/questions/${questionId}`,
        {
            method: "PUT",

            body: JSON.stringify(
                questionData
            )
        }
    );
};


export const deleteQuestion = async (
    questionId
) => {

    return apiRequest(
        `/questions/${questionId}`,
        {
            method: "DELETE"
        }
    );
};

export const startAttempt = async (
    quizId
) => {

    return apiRequest(
        "/attempts/start",
        {
            method: "POST",

            body: JSON.stringify({
                quiz_id: quizId
            })
        }
    );
};


export const saveAttemptAnswer = async (
    attemptId,
    questionId,
    answer
) => {

    return apiRequest(
        `/attempts/${attemptId}/answer`,
        {
            method: "PUT",

            body: JSON.stringify({
                question_id: questionId,
                answer
            })
        }
    );
};


export const resumeAttempt = async (
    attemptId
) => {

    return apiRequest(
        `/attempts/${attemptId}`,
        {
            method: "GET"
        }
    );
};


export const submitAttempt = async (
    attemptId,
    answers
) => {

    return apiRequest(
        `/attempts/${attemptId}/submit`,
        {
            method: "POST",

            body: JSON.stringify({
                answers
            })
        }
    );
};


export const getMyResults = async () => {

    return apiRequest(
        "/results/me",
        {
            method: "GET"
        }
    );
};


export const getResultById = async (
    resultId
) => {

    return apiRequest(
        `/results/${resultId}`,
        {
            method: "GET"
        }
    );
};


export const getResultBreakdown = async (
    resultId
) => {

    return apiRequest(
        `/results/${resultId}/breakdown`,
        {
            method: "GET"
        }
    );
};


export const getAdminResults = async () => {

    return apiRequest(
        "/results/admin/dashboard",
        {
            method: "GET"
        }
    );
};