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
    IconButton } from '@material-ui/core';
import { convertDateTimeFromServer } from 'app/shared/util/date-utils';

interface IAlbumProps {
    id: number;
    owner: string;
    name?: string;
    description?: string;
    date: Date;
    preview: string;
    categories?: [],
    tags? : []
}

const Album = (props: IAlbumProps) => {
    const classes = useStyles();
    return (
        <Card className={classes.card}>
        <CardHeader
            avatar={
            <Avatar aria-label="recipe" className={classes.avatar}>
                R
            </Avatar>
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
        <CardActions disableSpacing>
            <IconButton aria-label="add to favorites">
            <FavoriteIcon />
            </IconButton>
        </CardActions>
        </Card>
  );
}

export default Album;