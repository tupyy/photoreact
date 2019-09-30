import React from 'react';
import { IPhoto } from 'app/shared/model/photo';
import Photo from 'app/shared/components/photo/photo';
import { Theme, createStyles, makeStyles, useTheme } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import {Link} from '@material-ui/core';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { useCurrentWidth } from 'react-socks';

interface IPhotoContainer {
	photos: IPhoto[],
	selectedPhotos: IPhoto[],
	albumHRef: string
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
	
	function useWidth() {
	  const theme = useTheme();
	  const keys = [...theme.breakpoints.keys].reverse();
	  return (
			keys.reduce((output, key) => {
			  // eslint-disable-next-line react-hooks/rules-of-hooks
			const matches = useMediaQuery(theme.breakpoints.up(key));
			return !output && matches ? key : output;
			}, null) || 'xs'
	  );
	}

	const columnCount = () => {
		const width = useWidth();

		if (width === 'xs') {
			return 1;
		} else if (width === 'sm') {
			return 3;
		}
		return 6;
	}

	return (
		<div className={classes.root}>
		  <GridList cellHeight={160} className={classes.gridList} cols={columnCount()}>
			{props.photos.map( (photo:IPhoto, index: number) => (
			  <GridListTile key={index.toString()} cols={1} className={classes.tile}>
				  <Link href={props.albumHRef + 'photo/' + photo.id + '/'}>
					  <Photo 
					  url={photo.get_thumbnail_url} 
					  className={classes.photo}
				  />
				 </Link>
			  </GridListTile>
			))}
		  </GridList>
		</div>
	);
};

export default PhotoContainer;
