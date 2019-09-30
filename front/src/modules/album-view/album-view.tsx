import React, {useEffect} from 'react';
import {connect} from 'react-redux';
import {IRootState} from 'app/shared/reducers';
import {getPhotos} from 'app/shared/reducers/album';
import PhotoContainer from 'app/modules/album-view/photo-container';
import LoadingComponent from 'app/shared/components/loading/loading-component';

interface IAlbumView extends StateProps, DispatchProps {
	match: {}
}

export const AlbumView = (props: IAlbumView) => {
	useEffect( () => {
		props.getPhotos(props.match.params.id);
	}, []);


	const renderThumbnails = () => {
		if (props.photos) {
			return (
				<PhotoContainer 
					photos={props.photos}
					selectedPhotos={props.selectedPhotos}
					albumHRef={'album/' + props.match.params.id + '/'}
				/>);
		} else {
			return (<div>None</div>);
		}
	};

	return (
		<div>
			{ props.loading ? (
				<LoadingComponent />
			): (
				renderThumbnails()
			)}
		</div>
	)
};

const mapStateToProps = ({album}: IRootState) => ({
	loading: album.loading,
	errorMessage: album.errorMessage,
    album: album.album,
	photos: album.photos,
	mode: album.mode,
	selectedPhotos: album.selectedPhotos
});

const mapDispatchToProps =  {
	getPhotos
};

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(AlbumView)
