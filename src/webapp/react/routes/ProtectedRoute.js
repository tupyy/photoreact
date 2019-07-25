import React from 'react';
import {Redirect, Route, withRouter} from 'react-router';
import {connect} from "react-redux";

class ProtectedRoute extends React.Component {
    render() {
        const { component: Component, ...props } = this.props;

        return (
            <Route
                {...props}
                render={props => (
                    this.props.authentication.userAuthenticated ?
                        <Component {...props} /> :
                        <Redirect to='/login' />
                )}
            />
        )
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    }
};

export default connect(mapStateToProps)(ProtectedRoute);
