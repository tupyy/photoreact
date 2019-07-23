import {createReducers} from "./index";

const initialAuthenticationState = {
    userLogged: false,
    username: "",
    id: ""
};

const authenticationReducer = createReducers(initialAuthenticationState, {});

export default authenticationReducer;
