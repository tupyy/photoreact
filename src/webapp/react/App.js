import React from 'react';
import './App.css';
import {connect} from "react-redux";
import {AllRoutes} from './routes/AllRoutes';

class App extends React.Component {

    render() {
        return (
            <AllRoutes />
        );
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    }
};

export default connect(mapStateToProps)(App);
