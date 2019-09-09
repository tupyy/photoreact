import React, { useEffect } from 'react';
import {connect} from 'react-redux';
import {Redirect, RouteComponentProps} from 'react-router-dom';

import {IRootState} from 'app/shared/reducers';
import {login} from 'app/shared/reducers/authentication';
import {hideNavBar} from 'app/shared/reducers/navbar';
import LoginForm from './login-form';

export interface ILoginProps extends StateProps, DispatchProps, RouteComponentProps<{}> {}

export const Login = (props: ILoginProps) => {
    useEffect( () => {
        props.hideNavBar();
    }, [])

    const handleLogin = (username, password, rememberMe = false) => props.login(username, password, rememberMe);

    const { location, isAuthenticated } = props;
    const { from } = location.state || { from: { pathname: '/', search: location.search } };
    if (isAuthenticated) {
        return <Redirect to={from} />;
    }
    return <LoginForm handleLogin={handleLogin} loginError={props.loginError} />;
};

const mapStateToProps = ({ authentication, navbar }: IRootState) => ({
    isAuthenticated: authentication.isAuthenticated,
    loginError: authentication.loginError,
    navbar: navbar
});

const mapDispatchToProps = { 
    login,
    hideNavBar
};

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Login);
