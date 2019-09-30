import React from 'react';
import { IPhoto } from 'app/shared/model/photo';
import Photo from 'app/shared/components/photo/photo';
import { Theme, createStyles, makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { useCurrentWidth } from 'react-socks';

interface IPhotoContainer {
	photos: IPhoto[],
	selectedPhotos: IPhoto[],
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
		marginTop: 10,
      	overflow: 'hidden',
    },
    gridList: {
    },
	tile: {
		display: 'flex',
		justifyContent: 'center'
	},
	photo: {}
  }),
);


const PhotoContainer = (props: IPhotoContainer) => {
	const classes = useStyles();
	const width = useCurrentWidth();	
	
	const columnCount = (width:number) => {
		if (width < 600) {
			return 1;
		} else if (width > 600 && width < 900) {
			return 3;
		}
		return 6;
	}

	return (
		<div className={classes.root}>
		  <GridList cellHeight={160} className={classes.gridList} cols={columnCount(width)}>
			{props.photos.map( (photo:IPhoto, index: number) => (
			  <GridListTile key={index.toString()} cols={1} className={classes.tile}>
				  <Photo 
					  url={photo.get_thumbnail_url} 
					  className={classes.photo}
				  />
			  </GridListTile>
			))}
		  </GridList>
		</div>
	);
};

export default PhotoContainer;
