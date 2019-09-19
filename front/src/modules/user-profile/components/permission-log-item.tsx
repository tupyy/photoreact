import React from 'react';
import { Grid, makeStyles, Paper, Theme, Typography } from '@material-ui/core';
import {red, green, yellow} from '@material-ui/core/colors';
import {IPermissionLog} from 'app/shared/model/permission_log.model';
import moment from 'moment';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faImages, 
		faCalendarAlt, 
		faUser, 
		faUsers,
		faPlus,
		faPenAlt,
		faMinus
} from '@fortawesome/free-solid-svg-icons'
import {APP_LOCAL_DATETIME_FORMAT} from 'app/config/constants';

interface IPermissionLogItem {
	permissionLog: IPermissionLog
}

const useStyles = makeStyles( (theme:Theme) => ({
	root: {
		marginTop: 5,
		marginBottom: 5
	},
	iconContainer: {
		display: 'flex',
		justifyContent: 'center',
		alignItems: 'center'
	},
	mainContainer:{},
	dateAlbumContainer: {
		display: 'flex',
		justifyContent: 'left'
	},
	date: {
		paddingRight: 5
	},
	album: {},
	icon: {
		paddingRight: 5
	}

}));

const PermissionLogItem = (props: IPermissionLogItem) => {
	
	/**
     * Format the date from server to a simple format
     * @param date ISO INSTANT fromat
     */
    const formatDate = (dateString: string) : string => {
	    return moment(dateString).format(APP_LOCAL_DATETIME_FORMAT)
    }
	
	const renderActionIcon = (operation: string) => {
		switch(operation) {
			case 'add':
				return ( <FontAwesomeIcon icon={faPlus} /> );
			case 'modify':
				return (<FontAwesomeIcon icon={faPenAlt} /> );
			case 'delete':
				return (<FontAwesomeIcon icon={faMinus} /> );
		}
	};

	const getBackgroundColor = (operation: string) => {
		switch(operation) {
			case 'add':
				return green[100]; 
			case 'modify':
				return yellow[100];
			case 'delete':
				return red[100];
		}
	}
	const classes = useStyles();
	return (
		<div className={classes.root}> 
			<Paper
				elevation={0}
				style={{backgroundColor: getBackgroundColor(props.permissionLog.operation)}}>
				<Grid container>
					<Grid item className={classes.iconContainer} xs={2}>
						{renderActionIcon(props.permissionLog.operation)}
					</Grid>
					<Grid item xs container direction="column" className={classes.mainContainer} >
						<Grid item xs>
							<Typography gutterBottom variant="subtitle2">
								{props.permissionLog.contentObject.type === 'user' ? (
									<FontAwesomeIcon icon={faUser} className={classes.icon} />
								) : (
									<FontAwesomeIcon icon={faUsers} className={classes.icon} />
								)}
								<span> {props.permissionLog.contentObject.name} </span>
							</Typography>
							<div className={classes.dateAlbumContainer}>
								<div className={classes.date}>
									<Typography variant="body2">
										<FontAwesomeIcon icon={faCalendarAlt} className={classes.icon} />
										{props.permissionLog.date}
									</Typography>
								</div>
								<div className={classes.album}>
									<Typography variant="body2">
										<FontAwesomeIcon icon={faImages} className={classes.icon} />
										{props.permissionLog.album.name}
									</Typography>
								</div>
							</div>
						</Grid>
					</Grid>
					<Grid item>
						{props.permissionLog.permission}
					</Grid>
				</Grid>
			</Paper>
	</div>
		)
};

export default PermissionLogItem;
