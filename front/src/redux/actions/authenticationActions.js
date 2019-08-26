import {LOGIN_FAILED, LOGIN_SUCCESSFUL, LOGOUT_USER} from "./authenticationActionTypes";

export const LogoutUser = (id) => ({
    type: LOGOUT_USER,
    id: id
});

export const LoginSuccessful = (username, id) => ({
    type: LOGIN_SUCCESSFUL,
    username: username,
    id: id
});

export const LoginFailed = (reason) => ({
    type: LOGIN_FAILED,
    reason: reason
});


