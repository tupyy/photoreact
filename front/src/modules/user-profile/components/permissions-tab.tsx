import React, {useContext, useEffect} from 'react';
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles, Theme} from "@material-ui/core";
import combineStyles from "app/shared/util/combine-styles";
import useTabComponentStyles from "app/modules/user-profile/components/tab-component-styles";
import {IRootState} from 'app/shared/reducers';
import {connect} from 'react-redux';
import {getPermissionLogs} from 'app/shared/reducers/user-profile';
import {IPermissionLog} from 'app/shared/model/permission_log.model';
import LoadingComponent from 'app/shared/components/loading/loading-component';
import PermissionComponent from 'app/modules/user-profile/components/permission-component';

interface IPermissionsTab extends ITabComponent, StateProps, DispatchProps {}

const useStyles = combineStyles(useTabComponentStyles,makeStyles( (theme: Theme) => {

}));

const PermissionsTab: React.SFC<IPermissionsTab> = (props: IPermissionsTab) => {

    const tabContext = useContext(TabContext);

	useEffect( () => {
		// Load data only once when the tab becomes visible for the first time
		if (isVisible() && !hasData(props.permissionLogs) && !props.loading ) {
			props.getPermissionLogs();
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
	const hasData = (arr: Array<IPermissionLog>) => {
		return arr.length !== 0;
	};

	const classes = useStyles();
	/**
	 * Render loading component if component is visible and data is fetching
	 */
	if (isVisible() && props.loading) {
		return (
			<LoadingComponent />
		)
	}
	else if (isVisible() && hasData(props.permissionLogs)) {
		return (
			<div>
				<div>
					<PermissionComponent
						title="Permissions"
						data={props.permissionLogs}
					/>
				</div>
			</div>
			)
	}
	return (<div></div>);
};

const mapStateToProps = ({userProfile}: IRootState) => ({
	loading: userProfile.loading,
	permissionLogs: userProfile.permissionLog,
	errorMessage: userProfile.errorMessage
});

const mapDispatchToProps = {
	getPermissionLogs
};


type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(PermissionsTab);
