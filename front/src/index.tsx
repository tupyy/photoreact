import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { bindActionCreators } from 'redux';

import initStore from './config/store';
import setupAxiosInterceptors from './config/axios-interceptor';
import { clearAuthentication } from './shared/reducers/authentication';
import ErrorBoundary from './shared/error/error-boundary';
import AppComponent from './App';
import { loadIcons } from './config/icon-loader';

const store = initStore();

const actions = bindActionCreators({ clearAuthentication }, store.dispatch);
setupAxiosInterceptors(() => actions.clearAuthentication('login.error.unauthorized'));

loadIcons();

const rootEl = document.getElementById('root');

const render = Component =>
    ReactDOM.render(
        <ErrorBoundary>
            <Provider store={store}>
                <div>
                    <Component />
                </div>
            </Provider>
        </ErrorBoundary>,
        rootEl
    );

render(AppComponent);

