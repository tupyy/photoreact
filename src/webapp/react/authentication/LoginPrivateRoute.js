import React from "react";
import {Redirect, Route} from "react-router";
import {connect} from "react-redux";

export class LoginPrivateRoute extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <Route render={(props) => (
                true === true
                    ? <props.component {...props} />
                    : <Redirect to='/login'/>
            )}/>
        )
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    }
};
connect(mapStateToProps)(LoginPrivateRoute);
