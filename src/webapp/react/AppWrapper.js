import React from "react";
import {Redirect} from "react-router";
import {connect} from 'react-redux';

class AppWrapper extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.authentication.userAuthenticated === true) {
            return (
                <Redirect to='/home' />
            )
        } else {
            return (
                <Redirect to="/login" />
            )
        }
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    }
};

export default connect(mapStateToProps)(AppWrapper);
