import rootReducer from "./reducers";
import {createStore, applyMiddleware} from "redux";
import thunkMiddleware from "redux-thunk";

export default createStore(
    rootReducer,
    applyMiddleware(thunkMiddleware)
);
