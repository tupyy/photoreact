import React from 'react';
import './App.css';
import Home from "./Home";
import {BrowserRouter, Redirect, Route} from "react-router-dom";
import Login from "./authentication/Login";
import {connect} from "react-redux";

class App extends React.Component {

    render() {
        return (
            <BrowserRouter>
                <PrivateRoute path="/" component={Home} userLogged={this.props.authentication.userLogged} />
                <Route path="/login" component={Login} />
            </BrowserRouter>
        );
    }
}

const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route {...rest} render={(props) => (
        props.userLogged === true
            ? <Component {...props} />
            : <Redirect to='/login' />
    )} />
);

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    }
};

export default connect(mapStateToProps)(App);
