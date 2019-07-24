import {createReducers} from "./index";
import authenticationService from "../../services/authentication/userService";
import {loginUser} from "../actions/authenticationActions";

const initialAuthenticationState = {
    userAuthenticated: false,
    username: "",
    id: "",
};

const authenticationReducer = createReducers(initialAuthenticationState, {
    AUTHENTICATE: authenticate,
    LOGIN_USER: login
});

/**
 * Performs async authentication
 * @param username
 * @param password
 */
export function authenticate(username, password) {
    return function (dispatch) {
        return authenticationService(username, password)
            .then(val => dispatch(loginUser(val.username, val.id)));
    }
}

/**
 * Log in the user
 * @param state
 * @param action
 * @return {any}
 */
function login(state, action) {
    return Object.assign({}, state, {
        userAuthenticated: true,
        username: action.username,
        id: action.id
    });
}

export default authenticationReducer;
