import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import './index.css';
import * as serviceWorker from './serviceWorker';
import store from "./redux/store";
import App from "./react/App";
import './i18n';

const rootElement = document.getElementById('root');

const render = () => ReactDOM.render(
    <Provider store={store}>
        <App/>
    </Provider>,rootElement
);

render();
store.subscribe(render);
serviceWorker.unregister();
module.hot.accept();
