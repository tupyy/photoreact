import React from 'react';
import Card from "@material-ui/core/Card";
import IconButton from "@material-ui/core/IconButton";
import MoreVertIcon from '@material-ui/icons/MoreVert';
import FavoriteIcon from '@material-ui/icons/Favorite';
import PlayIcon from '@material-ui/icons/PlayArrow';
import CardMedia from "@material-ui/core/CardMedia";
import {CardContent, withStyles} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import styles from "./Album.module.css";
import CardHeader from "@material-ui/core/CardHeader";
import CardActions from "@material-ui/core/CardActions";

class Album extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const {classes, title,albumDate, albumImage, albumDescription} = this.props;
        return (
            <Card className={classes.card} >
                <CardHeader
                    action={
                        <IconButton>
                            <MoreVertIcon />
                        </IconButton>
                    }
                    title={title}
                    subheader={albumDate}
                />
                <CardMedia
                    className={classes.media}
                    image={albumImage}
                />
                <CardContent>
                    <Typography variant="body2" color="textSecondary" component="p">
                        {albumDescription}
                    </Typography>
                </CardContent>
                <CardActions disableSpacing>
                    <IconButton>
                        <PlayIcon className={classes.playIcon}/>
                    </IconButton>
                    <IconButton>
                        <FavoriteIcon />
                    </IconButton>
                </CardActions>
            </Card>
        )
    }
}

export default withStyles(styles)(Album)
