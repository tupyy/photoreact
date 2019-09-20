import React, {useContext,useEffect} from 'react';
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles, Theme} from "@material-ui/core";
import {IRootState} from 'app/shared/reducers';
import {getAlbums} from 'app/shared/reducers/user-profile';
import LoadingComponent from 'app/shared/components/loading/loading-component';
import {IAlbum} from 'app/shared/model/album.model';
import {connect} from 'react-redux';
import AlbumComponent from 'app/modules/user-profile/components/album-component';

interface IAlbumTabProps extends ITabComponent, StateProps, DispatchProps {}

const useStyles = makeStyles( (theme: Theme) => {

});

const AlbumsTab: React.SFC<IAlbumTabProps> = (props: IAlbumTabProps) => {
    const tabContext = useContext(TabContext);

	useEffect( () => {
		// Load data only once when the tab becomes visible for the first time
		if (isVisible() && !hasData(props.albums) && !props.loading ) {
			props.getAlbums();
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
	const hasData = (arr: Array<IAlbum>) => {
		return arr !== null;
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
	else if (isVisible() && hasData(props.albums)) {
		return (
			<div>
				<div className={classes.root}>
					<AlbumComponent
						title="Albums"
						data={props.albums}
					/>
				</div>
			</div>
			)
	}
	return (<div/>);
};

const mapStateToProps = ({userProfile}: IRootState) => ({
	loading: userProfile.loading,
	albums: userProfile.albums,
	errorMessage: userProfile.errorMessage
});

const mapDispatchToProps = {
	getAlbums
};

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AlbumsTab);
