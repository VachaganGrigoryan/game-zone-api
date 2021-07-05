import {LOGIN_FAIL, LOGIN_SUCCESS, LOGOUT, SIGNUP_FAIL, SIGNUP_SUCCESS} from "./types";

import AuthService from "../services/auth.service";

export const signup = (first_name, last_name, username, password) => (dispatch) => {
    return AuthService.signup(first_name, last_name, username, password).then(
        (response) => {
            dispatch({
                type: SIGNUP_SUCCESS,
            });

            // dispatch({
            //     type: SET_MESSAGE,
            //     payload: response.data.message,
            // });

            return Promise.resolve()
        },
        (error) => {
            const message =
                (error.response &&
                 error.response.data &&
                 error.response.data.message) ||
                error.message ||
                error.toString();

            dispatch({
                type: SIGNUP_FAIL,
            });

            // dispatch({
            //     type: SET_MESSAGE,
            //     payload: message,
            // });

            return Promise.reject();
        }
    );
}

export const login = (username, password) => (dispatch) => {
    return AuthService.login(username, password).then(
        (data) => {
            dispatch({
                type: LOGIN_SUCCESS,
                payload: {user: data}
            });

            return Promise.resolve();
        },
        (error) => {
            const message =
                (error.response &&
                    error.response.data &&
                    error.response.data.message) ||
                error.message ||
                error.toString();

            dispatch({
                type: LOGIN_FAIL
            });

            // dispatch({
            //     type: SET_MESSAGE,
            //     payload: message,
            // });

            return Promise.resolve();
        }
    );
}

export const logout = () => (dispatch) => {
    AuthService.logout();

    dispatch({
        type: LOGOUT
    });
}