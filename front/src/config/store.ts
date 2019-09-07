import { createStore, applyMiddleware, compose } from 'redux';
import promiseMiddleware from 'redux-promise-middleware';
import thunkMiddleware from 'redux-thunk';
import reducer, { IRootState } from 'app/shared/reducers';
import DevTools from './devtools';
import errorMiddleware from './error-middleware';
import loggerMiddleware from './logger-middleware';

const defaultMiddlewares = [
  thunkMiddleware,
  errorMiddleware,
  promiseMiddleware,
  loggerMiddleware
];

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const composedMiddlewares = middlewares =>
  process.env.NODE_ENV === 'development'
    ? composeEnhancers(
        applyMiddleware(...defaultMiddlewares, ...middlewares),
      )
    : compose(
        applyMiddleware(...defaultMiddlewares, ...middlewares)
      );

const initialize = (initialState?: IRootState, middlewares = []) => createStore(
    reducer,
    initialState,
    composedMiddlewares(middlewares));

export default initialize;
