import axios from 'axios';
import React, {useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core';
import { CircularProgress } from '@material-ui/core';

export interface IPhotoProps {
    url: string;
    name?: string;
    className: any;
}

const useStyles = makeStyles(theme => ({
    progress: {
        margin: theme.spacing(2),
      },
}));

export default function Photo(props: IPhotoProps) {
    const [loading, setLoading] = useState(true);

    const classes = useStyles();
    return (
        <div>
            <img className={props.className} src={props.url} onLoad={() => setLoading(false)} alt={props.name} />
            {loading && 
                <CircularProgress className={classes.progress} />
            }
        </div>
    )
}