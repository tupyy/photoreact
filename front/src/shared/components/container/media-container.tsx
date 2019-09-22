import React  from 'react';
import {Grid, Paper} from '@material-ui/core';
import useStyles from 'app/shared/components/container/media-container-styles';

export interface IContainerProps {
	component: React.SFC<any>,
	data: any[], 
};

const MediaContainer = (props: IContainerProps) => {

    const classes = useStyles();
    return (
        <Grid container className={classes.root} spacing={2}>
            <Paper>
            <Grid item xs={12}>
                <Grid container justify="center" spacing={2}>
                    {props.data.map( (entry: {}, index: number) =>
					<Grid key={index.toString()} item>
						<props.component 
							data={entry}
						/>
                    </Grid>
                    )}
                </Grid>
            </Grid>
            </Paper>
        </Grid>
    )
};

export default MediaContainer;
