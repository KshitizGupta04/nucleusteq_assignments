import API_ENDPOINTS from "../constants/apiEndpoints";

import {
    deleteRequest,
    get,
    post,
    put
} from "./api";


export const getCategories = async () => {

    return get(
        API_ENDPOINTS.CATEGORIES.BASE
    );
};


export const getCategoryById = async (
    categoryId
) => {

    return get(
        API_ENDPOINTS.CATEGORIES.BY_ID(
            categoryId
        )
    );
};


export const createCategory = async (
    name,
    description
) => {

    return post(
        API_ENDPOINTS.CATEGORIES.BASE,
        {
            name,
            description
        }
    );
};


export const updateCategory = async (
    categoryId,
    name,
    description
) => {

    return put(
        API_ENDPOINTS.CATEGORIES.BY_ID(
            categoryId
        ),
        {
            name,
            description
        }
    );
};


export const deleteCategory = async (
    categoryId
) => {

    return deleteRequest(
        API_ENDPOINTS.CATEGORIES.BY_ID(
            categoryId
        )
    );
};


export const getQuizzes = async () => {

    return get(
        API_ENDPOINTS.QUIZZES.BASE
    );
};


export const createQuiz = async (
    quizData
) => {

    return post(
        API_ENDPOINTS.QUIZZES.BASE,
        quizData
    );
};


export const updateQuiz = async (
    quizId,
    quizData
) => {

    return put(
        API_ENDPOINTS.QUIZZES.BY_ID(
            quizId
        ),
        quizData
    );
};


export const deleteQuiz = async (
    quizId
) => {

    return deleteRequest(
        API_ENDPOINTS.QUIZZES.BY_ID(
            quizId
        )
    );
};


export const getAdminQuestionsByQuiz = async (
    quizId
) => {

    return get(
        API_ENDPOINTS.QUESTIONS.ADMIN_BY_QUIZ(
            quizId
        )
    );
};


export const getQuestionsByQuiz = async (
    quizId
) => {

    return get(
        API_ENDPOINTS.QUESTIONS.BY_QUIZ(
            quizId
        )
    );
};


export const createQuestion = async (
    questionData
) => {

    return post(
        API_ENDPOINTS.QUESTIONS.BASE,
        questionData
    );
};


export const updateQuestion = async (
    questionId,
    questionData
) => {

    return put(
        API_ENDPOINTS.QUESTIONS.BY_ID(
            questionId
        ),
        questionData
    );
};


export const deleteQuestion = async (
    questionId
) => {

    return deleteRequest(
        API_ENDPOINTS.QUESTIONS.BY_ID(
            questionId
        )
    );
};


export const getAdminResults = async () => {

    return get(
        API_ENDPOINTS.RESULTS.ADMIN_DASHBOARD
    );
};


export const getQuizStatistics = async (
    quizId
) => {

    return get(
        API_ENDPOINTS.RESULTS.QUIZ_STATISTICS(
            quizId
        )
    );
};


export const getQuizLeaderboard = async (
    quizId
) => {

    return get(
        API_ENDPOINTS.RESULTS.QUIZ_LEADERBOARD(
            quizId
        )
    );
};

export const getResultBreakdown = async (
    resultId
) => {

    return get(
        API_ENDPOINTS.RESULTS.BREAKDOWN(
            resultId
        )
    );
};