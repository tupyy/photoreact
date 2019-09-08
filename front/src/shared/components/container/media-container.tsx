import React, {useEffect, useState, Dispatch} from 'react';
import {getRecentAlbums} from 'app/shared/reducers/media';
import {IRootState} from 'app/shared/reducers';
import Album from 'app/shared/components/album/album';
import { connect } from 'react-redux';

export interface IContainerProps extends StateProps, DispatchProps {}

const MediaContainer = (props: IContainerProps) => {
    useEffect( () => {
        props.getRecentAlbums();
    }, []);

    const Albums = props.albums.map( (album) => 
        <Album 
            key = {String(album.id)}
            id = {album.id}
            owner = {album.owner}
            date = {album.date}
            preview = {album.preview}
            name = {album.name}
            description = {album.description}
        />
    )

    return (
        <div>
            {Albums}
        </div>
    )
}

const mapStateToProps = ({media} : IRootState) => ({
    albums: media.recentAlbums
});

const mapDispatchToProps = { getRecentAlbums };

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(MediaContainer);

