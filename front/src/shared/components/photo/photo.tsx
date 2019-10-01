import React, {useState} from 'react';
import { makeStyles } from '@material-ui/core';
import { CircularProgress } from '@material-ui/core';

export interface IPhotoProps {
    url: string;
    name?: string;
	selected: boolean;
}

const useStyles = makeStyles(theme => ({
    progress: {
        margin: theme.spacing(2),
      },
	photo: {},
	selected: {
	}
}));

export default function Photo(props: IPhotoProps) {
    const [loading, setLoading] = useState(true);

    const classes = useStyles();
	const selected = props.selected ? classes.selected : '';
	const imgClass = `${classes.photo} ${selected}`;
    return (
        <div>
            <img className={imgClass} src={props.url} onLoad={() => setLoading(false)} alt={props.name} />
            {loading && 
                <CircularProgress className={classes.progress} />
            }
        </div>
    )
}
