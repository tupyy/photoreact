import React, {useContext} from 'react';
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles} from "@material-ui/core";
import {Theme} from "@material-ui/core/styles/createMuiTheme";
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import LoadingComponent from 'app/shared/components/loading/loading-component';
import AlbumTab from 'app/modules/user-profile/components/albums-tab';
import ActivityTab from 'app/modules/user-profile/components/activities-tab';
import {IRootState} from 'app/shared/reducers';
import {connect} from 'react-redux';

interface IOverview extends ITabComponent,StateProps {
}

const useStyles = makeStyles( (theme: Theme) => ({
}));

export const Overview: React.SFC<IOverview> = (props: IOverview) => {
    const tabContext = useContext(TabContext);

	/**
	 * Return true if the component is visible
	 */
	const isVisible = () => {
		return props.index === tabContext.currentTab; 
	}

    // @ts-ignore
    const classes = useStyles();
	if (isVisible() && props.loading) {
		return (
			<LoadingComponent />
		)
	} else {
    	return (
    	    <div> 
				<AlbumTab
					index={props.index}
				/>
				<ActivityTab
					index={props.index}
				/>
    	    </div>
    	)
	}
};


const mapStateToProps = ({userProfile}: IRootState) => ({
	loading: userProfile.loading,
	errorMessage: userProfile.errorMessage
});


type StateProps = ReturnType<typeof mapStateToProps>;

export default connect(
	mapStateToProps,
)(Overview);

