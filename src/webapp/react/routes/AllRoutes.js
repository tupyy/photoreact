import React from "react";
import {Route} from "react-router";
import Login from "../authentication/Login";
import Home from "../Home";
import ProtectedRoute from "./ProtectedRoute";
import {BrowserRouter} from "react-router-dom";

export class AllRoutes extends React.Component {
    render() {
        return (
            <BrowserRouter>
                    <Route exact path='/login' component={Login} />
                    <ProtectedRoute exact path='/' component={Home} />
            </BrowserRouter>

        )
    }
}
