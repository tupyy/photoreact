import React, {useContext, useEffect} from 'react';
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles} from "@material-ui/core";
import {Theme} from "@material-ui/core/styles/createMuiTheme";
import {IActivity} from 'app/shared/model/activity.model';
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import LoadingComponent from 'app/shared/components/loading/loading-component';
import combineStyles from "app/shared/util/combine-styles";
import useTabComponentStyles from "app/modules/user-profile/components/tab-component-styles";
import ActivityComponent from 'app/modules/user-profile/components/activity-component';
import {IRootState} from 'app/shared/reducers';
import {getActivities} from 'app/shared/reducers/user-profile';
import {connect} from 'react-redux';

interface IActivityProps extends ITabComponent, StateProps, DispatchProps {}

const useStyles = combineStyles(useTabComponentStyles, makeStyles( (theme: Theme) => ({
})));

const Activity: React.SFC<IActivityProps> = (props: IActivityProps) => {
    const tabContext = useContext(TabContext);

	useEffect( () => {
		// Load data only once when the tab becomes visible for the first time
		if (isVisible() && !hasData(props.activities) && !props.loading ) {
			props.getActivities();
		}
	});

	/**
	 * Return true if the component is visible
	 */
	const isVisible = () => {
		return props.index === tabContext.currentTab; 
	}

	/**
	 * Return true if data has been fetched from server
	 */
	const hasData = (arr: Array<IActivity>) => {
		return arr.length !== 0;
	};

    // @ts-ignore
    const classes = useStyles();

	/**
	 * Render loading component if component is visible and data is fetching
	 */
	if (isVisible() && props.loading) {
		return (
			<LoadingComponent />
		)
	}
	else if (isVisible() && hasData(props.activities)) {
		return (
			<div>
				<div className={classes.root}>
					<ActivityComponent
						title="Activities"
						data={props.activities}
					/>
				</div>
			</div>
			)
	}
	return (<div></div>);
};

const mapStateToProps = ({userProfile}: IRootState) => ({
	loading: userProfile.loading,
	activities: userProfile.activities,
	errorMessage: userProfile.errorMessage
});

const mapDispatchToProps = {
	getActivities
};

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Activity);
