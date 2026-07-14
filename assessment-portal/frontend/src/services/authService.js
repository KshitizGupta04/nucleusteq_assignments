import {
    encryptPassword
} from "../utils/passwordEncryption";

import API_ENDPOINTS from "../constants/apiEndpoints";

import {
    get,
    post
} from "./api";


export const loginUser = async (
    username,
    password
) => {

    const encryptedPassword = (
        await encryptPassword(
            password
        )
    );


    return post(
        API_ENDPOINTS.AUTH.LOGIN,
        {
            username,
            password: encryptedPassword
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


    return post(
        API_ENDPOINTS.AUTH.REGISTER,
        {
            username,
            email,
            password: encryptedPassword
        }
    );
};


export const getMyProfile = async () => {

    return get(
        API_ENDPOINTS.AUTH.PROFILE
    );
};