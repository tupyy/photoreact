import React, {useState} from 'react';
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
    id: number;
    owner: string;
    name?: string;
    description?: string;
    date: Date;
    preview: string;
    isFavorite: boolean;
    categories?: [],
    tags? : []
}

const Album = (props: IAlbumProps) => {
    const classes = useStyles();
    return (
        <Card className={classes.card}>
        <CardHeader
            avatar={
            <UserAvatar 
                firstName={props.owner.first_name}
                lastName={props.owner.last_name}
                profilePhoto={props.owner.photo}
            />
            }
            action={
                <IconButton aria-label="favorites" color={props.isFavorite ? "secondary" : "disabled"}>
                   <FavoriteIcon /> 
                </IconButton>
            }
            title={props.name}
            subheader={convertDateTimeFromServer(props.date)}
        />
        <Photo className={classes.media} url={props.preview} />
        <CardContent>
            <Typography variant="body2" color="textSecondary" component="p">
                {props.description}
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