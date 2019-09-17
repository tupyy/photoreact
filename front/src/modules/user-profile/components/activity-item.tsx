import { Chip, Grid, makeStyles, Paper, Theme, Typography, Button } from '@material-ui/core';
import { blue, green, lime, red } from '@material-ui/core/colors';
import moment from 'moment';
import React from 'react';
import {APP_LOCAL_DATETIME_FORMAT} from 'app/config/constants';

interface IActivityItem {
    id: number,
    title: string,
    date: string,
    user: string,
    activity: string
}

// @ts-ignore
const useStyles = makeStyles( (theme: Theme) => ({
    root: {
        display: 'block',
        margin: 'auto'
    },
    paper: {
        paddingTop: '5px',
        paddingBottom: '5px',
        marginTop: '10px',
        borderBottom: '1px solid #f0f0f0',
        lineHeight: '20px'

    },
    titleContainer: {
        display: 'flex',
        alignContent: 'left',
        marginBottom: 5
    },
    owner: {
		display: 'flex',
		alignItems: 'center',
        paddingLeft: '5px',
        color: '#707070'
    },
    textContainer: {},
    title: {
        fontWeight: 'bold'
    },
    date: {
        marginBottom: 5
    },
    chipContainer: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
    },
    chip: {
        color: 'black',
        fontWeight: 'bold',
        border: '1px solid #f0f0f0',
    }
}));


const getChipData = (char: string):Object => {
    switch(char) {
        case 'V':
            return {label: 'Viewed',
                    color: blue[300]};
        case 'U':
            return {label: 'Updated',
                    color: lime[400]};
        case 'C':
            return {label: 'Created',
                    color: green[300]};
        case 'D':
            return {label: 'Deleted',
                    color: red[300]}
    }
}

const ActivityItem = (props:IActivityItem) => {

    const chipData = getChipData(props.activity);
    const location = '/album/' + String(props.id) + '/';

    /**
     * Format the date from server to a simple format
     * @param date ISO INSTANT fromat
     */
    const formatDate = (dateString: string) : string => {
	    return moment(dateString).format(APP_LOCAL_DATETIME_FORMAT)
    }
    
    
    // @ts-ignore
    const classes = useStyles(chipData.color);
    return (
        <div className={classes.root}>
            <Paper 
                elevation={0}
                className={classes.paper}>
                <Grid container spacing={2}>
                    <Grid item className={classes.textContainer} xs={10}>
                        <div className={classes.titleContainer}>
							<Button 
								variant="contained"
								size="small"
								className={classes.title}
								href={location}
							>
                                {props.title}
                            </Button>
                            <Typography className={classes.owner}>
                                @{props.user}
                            </Typography>
                        </div>
                        <Typography className={classes.date}>
                            {formatDate(props.date)}
                        </Typography>
                    </Grid>
                    <Grid item className={classes.chipContainer} xs={2} xl={2}>
                         <Chip className={classes.chip}
                            color="primary" 
                            size="small"
                            style={{'backgroundColor': chipData.color}}
                            label={chipData.label} />
                    </Grid>
                </Grid>
            </Paper>
        </div>   
    )
};

export default ActivityItem;
