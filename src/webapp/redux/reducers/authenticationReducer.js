import {createReducers} from "./index";

const initialAuthenticationState = {
    isLogged: false,
    username: "",
    id: ""
};

const authenticationReducer = createReducers(initialAuthenticationState, {});

export default authenticationReducer;
