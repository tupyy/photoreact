import React from 'react';
import Navbar from './navbar/Navbar';
import {connect} from "react-redux";

export default class Home extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Navbar />
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    };
};

connect(mapStateToProps)(Home);
