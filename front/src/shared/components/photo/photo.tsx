import React, {useState} from 'react';
import { makeStyles } from '@material-ui/core';
import { CircularProgress } from '@material-ui/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle } from '@fortawesome/free-regular-svg-icons/faCheckCircle';

export interface IPhotoProps {
    url: string;
    name?: string;
	selected: boolean;
}

const useStyles = makeStyles(theme => ({
    progress: {
        margin: theme.spacing(2),
      },
	  photo: {
		  position: 'relative'
	},
	selectedPhoto: {
		position: 'relative',
		opacity: 0.5
	},
	selectionIcon: {
		position: 'absolute',
		top: '30%',
		left: '50%',
		zIndex: 100,
		width: 100,
		height: 100,
		color: 'green',
	}
}));

export default function Photo(props: IPhotoProps) {
    const [loading, setLoading] = useState(true);

    const classes = useStyles();
	const selected = props.selected ? classes.selectionIcon : '';

	const renderSelectedPhoto = () => {
		return (
			<div>
				<FontAwesomeIcon icon={faCheckCircle} className={classes.selectionIcon} size="lg" />
				<img className={classes.selectedPhoto} src={props.url} onLoad={() => setLoading(false)} alt={props.name} />
			</div>
		);
	}

	return (
        <div>
			{selected ? ( renderSelectedPhoto() ) : (
	            <img className={classes.photo} src={props.url} onLoad={() => setLoading(false)} alt={props.name} />
			)}
            {loading && 
                <CircularProgress className={classes.progress} />
            }
        </div>
    )
}
