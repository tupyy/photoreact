import { Chip, Grid, makeStyles, Divider, Theme, Typography, Button } from '@material-ui/core';
import moment from 'moment';
import React from 'react';
import {APP_LOCAL_DATETIME_FORMAT} from 'app/config/constants';
import {IAlbum} from 'app/shared/model/album.model';

export interface IAlbumItemProps {
	album: IAlbum

	// if true show categories 
	hasCategories: boolean,

	// show tags
	hasTags: boolean
}

// @ts-ignore
const useStyles = makeStyles( (theme: Theme) => ({
	root: {
	  display: 'block',
	  margin: 'auto',
      width: '100%',
      backgroundColor: theme.palette.background.paper,
    },
    chip: {
      marginRight: theme.spacing(1),
    },
    section1: {
      paddingTop: '5px',
      marginTop: '10px',
      lineHeight: '20px'
    },
    section2: {
      margin: theme.spacing(1),
    },
    section3: {
      margin: theme.spacing(3, 1, 1),
    },
	buttonContainer: {
		paddingBottom: '5px'
	},
	button: {
		fontWeight: 'bold'
	}
}));


const AlbumItem = (props:IAlbumItemProps) => {

    const location = '/album/' + String(props.album.id) + '/';

    /**
     * Format the date from server to a simple format
     * @param date ISO INSTANT fromat
     */
    const formatDate = (dateString: string) : string => {
	    return moment(dateString).format(APP_LOCAL_DATETIME_FORMAT)
    }
    
    const renderCategories = (categories: string[]) => {
		return (
			<div className={classes.section2}>
				{categories.map( (category:string, index:number) => 
						<Chip 
							key={index.toString()}
							className={classes.chip}
							color='primary'
							label={category} 
						/>
				)}
			</div>	
		)	
	};

	const renderTags = (tags: string[]) => {
		return (
			<div className={classes.section2}>
				{tags.map( (tag:string, index:number) => 
					  <Chip 
						  key={index.toString()}
						  className={classes.chip}
						  color='secondary'
						  label={tag} 
					  />
				)}
			</div>
		)
	}

    // @ts-ignore
    const classes = useStyles();
    return (
        <div className={classes.root}>
			<div className={classes.section1}>
                <Grid container alignItems="center" className={classes.buttonContainer} >
                    <Grid item xs >
						<Button 
							variant="contained" 
							size="small"
							href={location} 
							className={classes.button}>
							{props.album.name}
						</Button>
					</Grid>
					<Grid item>
						<Typography gutterBottom variant="subtitle2">
							{formatDate(String(props.album.date))}
						</Typography>
					</Grid>
				</Grid>
				<Typography color="textSecondary" variant="body2">
					{props.album.description}
					</Typography>
			</div>
			{props.hasCategories && 
				renderCategories(props.album.categories)
			}
			{props.hasTags &&
				renderTags(props.album.tags)
			}
			<Divider variant="middle" />
        </div>   
    )
};

export default AlbumItem;
