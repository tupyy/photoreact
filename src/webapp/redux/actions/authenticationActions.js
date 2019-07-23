import {LOGIN_FAILED, LOGIN_SUCCESSFUL, LOGIN_USER, LOGOUT_USER} from "./authenticationActionTypes";

export const LoginUser = (username, password) => ({
   type: LOGIN_USER,
   username: username,
   password: password
});

export const LogoutUser = (id) => ({
    type: LOGOUT_USER,
    id: id
});

export const LoginSuccessful = (username, id) => ({
    type: LOGIN_SUCCESSFUL,
    username: username,
    id: id
});

export const LoginFailed = (username) => ({
    type: LOGIN_FAILED,
    username: username
});
