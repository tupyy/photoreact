import React from 'react';
import { Paper, Grid, Typography, Chip, makeStyles, Theme, createMuiTheme } from '@material-ui/core';
import {red, blue, lime, green} from '@material-ui/core/colors';
import {Link} from 'react-router-dom';

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
        paddingBottom: '5px'
        marginTop: '10px',
        borderBottom: '1px solid #f0f0f0',
        lineHeight: '20px'

    },
    titleContainer: {
        display: 'flex'
        alignContent: 'left',
        marginBottom: 5
    },
    owner: {
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
    const location = {
        pathname: '/album/' + String(props.id) + '/'
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
                            <Typography className={classes.title}>
                                <Link to={location}>
                                    {props.title}
                                </Link>
                            </Typography>
                            <Typography className={classes.owner}>
                                @{props.user}
                            </Typography>
                        </div>
                        <Typography className={classes.date}>
                            {props.date}
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