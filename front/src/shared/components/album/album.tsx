import React, {useState} from 'react';
import {IAlbum} from 'app/shared/model/album.model';
import FavoriteIcon from '@material-ui/icons/Favorite';
import Photo from 'app/shared/components/photo/photo';
import useStyles from './album-styles';
import { Avatar, 
    Card, 
    CardHeader, 
    CardMedia, 
    CardContent,
    Typography,
    CardActions,
    IconButton, 
    Button} from '@material-ui/core';
import { convertDateTimeFromServer } from 'app/shared/util/date-utils';
import UserAvatar from 'app/shared/components/user_avatar/user-avatar';

interface IAlbumProps {
	data: IAlbum
}

const Album = (props: IAlbumProps) => {
    const classes = useStyles();
    return (
        <Card className={classes.card}>
        <CardHeader
            avatar={
            <UserAvatar 
                firstName={props.data.owner.first_name}
                lastName={props.data.owner.last_name}
                profilePhoto={props.data.owner.photo}
            />
            }
            action={
                <IconButton aria-label="favorites" color={props.data.isFavorite ? "secondary" : "disabled"}>
                   <FavoriteIcon /> 
                </IconButton>
            }
            title={props.data.name}
            subheader={convertDateTimeFromServer(props.data.date)}
        />
        <Photo className={classes.media} url={props.data.preview} />
        <CardContent>
            <Typography variant="body2" color="textSecondary" component="p">
                {props.data.description}
            </Typography>
        </CardContent>
        <CardActions className={classes.cardActions} disableSpacing>
            <Button color="primary" variant="contained">
                View
            </Button>
        </CardActions>
        </Card>
  );
}

export default Album;
