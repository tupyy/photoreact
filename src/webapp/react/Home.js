import React from 'react';
import Navbar from './components/Navbar/Navbar';
import {connect} from "react-redux";
import AlbumCard from "./components/AlbumCard/AlbumCard";

export default class Home extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Navbar />
                <AlbumCard title="Casa" albumDate="20 Iulie 2019" albumDescription="Lucrari in casa"/>
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
