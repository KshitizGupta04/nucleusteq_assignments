import API_ENDPOINTS from "../constants/apiEndpoints";

import {
    get,
    post,
    put
} from "./api";


export const getCategories = async () => {

    return get(
        API_ENDPOINTS.CATEGORIES.BASE
    );
};


export const getQuizzes = async () => {

    return get(
        API_ENDPOINTS.QUIZZES.BASE
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


export const startAttempt = async (
    quizId
) => {

    return post(
        API_ENDPOINTS.ATTEMPTS.START,
        {
            quiz_id: quizId
        }
    );
};


export const saveAttemptAnswer = async (
    attemptId,
    questionId,
    answer
) => {

    return put(
        API_ENDPOINTS.ATTEMPTS.ANSWER(
            attemptId
        ),
        {
            question_id: questionId,
            answer
        }
    );
};


export const resumeAttempt = async (
    attemptId
) => {

    return get(
        API_ENDPOINTS.ATTEMPTS.BY_ID(
            attemptId
        )
    );
};


export const submitAttempt = async (
    attemptId,
    answers
) => {

    return post(
        API_ENDPOINTS.ATTEMPTS.SUBMIT(
            attemptId
        ),
        {
            answers
        }
    );
};


export const getMyResults = async () => {

    return get(
        API_ENDPOINTS.RESULTS.MY_RESULTS
    );
};


export const getResultById = async (
    resultId
) => {

    return get(
        API_ENDPOINTS.RESULTS.BY_ID(
            resultId
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