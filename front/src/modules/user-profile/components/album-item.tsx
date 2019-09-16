import { Chip, Grid, makeStyles, Paper, Theme, Typography } from '@material-ui/core';
import { blue, green, lime, red } from '@material-ui/core/colors';
import moment from 'moment';
import React from 'react';
import { Link } from 'react-router-dom';
import {APP_LOCAL_DATETIME_FORMAT} from 'app/config/constants';
import {IAlbum} from 'app/shared/model/album.model';
import Photo from 'app/shared/components/photo/photo';

export interface IAlbumItemProps {
	album: IAlbum
}

// @ts-ignore
const useStyles = makeStyles( (theme: Theme) => ({
    root: {
        display: 'block',
        margin: 'auto'
    },
    paper: {
        paddingTop: '5px',
        paddingBottom: '5px',
        marginTop: '10px',
        borderBottom: '1px solid #f0f0f0',
        lineHeight: '20px'

    },
    nameContainer: {
        display: 'block',
        marginBottom: 5
    },
    owner: {
        paddingLeft: '5px',
        color: '#707070'
    },
    textContainer: {},
    photo: {
        fontWeight: 'bold'
    },
    date: {
        marginBottom: 5
    },
    chipContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
    },
    chip: {
        color: 'black',
        fontWeight: 'bold',
        border: '1px solid #f0f0f0',
    }
}));


const AlbumItem = (props:IAlbumItemProps) => {

    const location = {
        pathname: '/album/' + String(props.album.id) + '/'
    }

    /**
     * Format the date from server to a simple format
     * @param date ISO INSTANT fromat
     */
    const formatDate = (dateString: string) : string => {
	    return moment(dateString).format(APP_LOCAL_DATETIME_FORMAT)
    }
    
    
    // @ts-ignore
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <Paper 
                elevation={0}
                className={classes.paper}>
                <Grid container spacing={2}>
                    <Grid item className={classes.textContainer} xs={4}>
                        <div className={classes.nameContainer}>
                            <Link to={location}>
								<Typography className={classes.name} >
									{props.album.name}
								</Typography>
                            </Link>
							<Typography className={classes.date}>
                        	    {formatDate(String(props.album.date))}
                        	</Typography>
                        </div>
					</Grid>
                    <Grid item className={classes.chipContainer} xs={2} xl={2}>
                    </Grid>
                </Grid>
            </Paper>
        </div>   
    )
};

export default AlbumItem;
