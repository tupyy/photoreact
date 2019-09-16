import './App.scss';

import React, {useEffect} from 'react';
import {connect} from 'react-redux';
import {BrowserRouter as Router} from 'react-router-dom';
import {hot} from 'react-hot-loader';

import {IRootState} from 'app/shared/reducers';
import {getSession} from 'app/shared/reducers/authentication';
import {setLocale} from 'app/shared/reducers/locale';
import {hasAnyAuthority} from 'app/shared/auth/private-route';
import ErrorBoundary from 'app/shared/error/error-boundary';
import Header from 'app/shared/layout/header/header';
import {AUTHORITIES} from 'app/config/constants';
import AppRoutes from 'app/routes';

const baseHref = document
    .querySelector('base')
    .getAttribute('href')
    .replace(/\/$/, '');

export interface IAppProps extends StateProps, DispatchProps {}

export const App = (props: IAppProps) => {
    useEffect(() => {
        props.getSession();
    }, []);

    return (
        <Router basename={baseHref}>
            <ErrorBoundary>
                <Header isAuthenticated={true} isAdmin={false} showNavBar={true} />
            </ErrorBoundary>
            <div className="app-container">
                <div className="container-fluid view-container" id="app-view-container">
                    <ErrorBoundary>
                        <AppRoutes />
                    </ErrorBoundary>
                </div>
            </div>
        </Router>
    );
};

const mapStateToProps = ({ authentication, locale }: IRootState) => ({
    currentLocale: locale.currentLocale,
    IsAuthenticated: authentication.isAuthenticated,
    isAdmin: hasAnyAuthority(authentication.account.roles, [AUTHORITIES.ADMIN]),
});

const mapDispatchToProps = { setLocale, getSession };

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(hot(module)(App));

