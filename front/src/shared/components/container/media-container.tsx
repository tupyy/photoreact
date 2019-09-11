import React, { useEffect, useState, Dispatch } from 'react';
import { getRecentAlbums } from 'app/shared/reducers/album';
import { IRootState } from 'app/shared/reducers';
import Album from 'app/shared/components/album/album';
import { connect } from 'react-redux';
import useStyles from './media-container';
import { Grid, Paper } from '@material-ui/core';

export interface IContainerProps extends StateProps, DispatchProps { }

const MediaContainer = (props: IContainerProps) => {
    useEffect(() => {
        props.getRecentAlbums();
    }, []);

    const classes = useStyles();
    return (
        <Grid container className={classes.root} spacing={2}>
            <Paper>
            <Grid item xs={12}>
                <Grid container justify="center" spacing={2}>
                    {props.albums.map( (album) =>
                    <Grid key={String(album.id)} item>
                        <Album
                            id={album.id}
                            owner={album.owner}
                            date={album.date}
                            preview={album.preview}
                            name={album.name}
                            description={album.description}
                            isFavorite={true}
                        />
                    </Grid>
                    )}
                </Grid>
            </Grid>
            </Paper>
        </Grid>
    )
}

const mapStateToProps = ({ album }: IRootState) => ({
    albums: album.recentAlbums
});

const mapDispatchToProps = { getRecentAlbums };

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(MediaContainer);

