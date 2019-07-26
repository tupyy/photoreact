import {createReducers} from "./index";
import authenticationService from "../../services/authentication/userService";
import {LoginFailed, LoginSuccessful} from "../actions/authenticationActions";

const initialAuthenticationState = {
    userAuthenticated: true, //FIX temporary
    username: "",
    id: "",
    loginFailed: false
};

const authenticationReducer = createReducers(initialAuthenticationState, {
    AUTHENTICATE: authenticate,
    LOGIN_SUCCESSFUL: loginSuccessful,
    LOGIN_FAILED: loginFailed
});

/**
 * Performs async authentication
 * @param username
 * @param password
 */
export function authenticate(username, password) {
    return function (dispatch) {
        return authenticationService(username, password)
            .then(val => dispatch(LoginSuccessful(val.username, val.id)))
            .catch(() => dispatch(LoginFailed()));
    }
}

/**
 * Log in the user
 * @param state
 * @param action
 * @return {any}
 */
function loginSuccessful(state, action) {
    return Object.assign({}, state, {
        userAuthenticated: true,
        username: action.username,
        id: action.id
    });
}

function loginFailed(state) {
    return Object.assign({},state, {
        userAuthenticated: false,
        loginFailed: true
    })
}
export default authenticationReducer;
