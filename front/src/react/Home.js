import React from 'react';
import Navbar from './components/Navbar/Navbar';
import {connect} from "react-redux";
import AlbumContainer from "./components/AlbumContainer/AlbumContainer";

export default class Home extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Navbar/>
                <AlbumContainer
                    columns = {3}
                    rows = {1}
                    source = this.props.favoritesAlbums
                />
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication,
        favoritesAlbums: state.albums.favorites
    };
};

connect(mapStateToProps)(Home);
