import authenticationReducer from "./authenticationReducer";
import {combineReducers} from "redux";

export function createReducers(initialState, handlers) {
    return function reducer(state = initialState, action) {
        if (handlers.hasOwnProperty(action.type)) {
            return handlers[action.type](state, action)
        } else {
            return state
        }
    }
}

const rootReducer = combineReducers({
    authentication: authenticationReducer
});

export default rootReducer;
