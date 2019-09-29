import React from 'react';
import {connect} from 'react-redux';
import {IRootState} from 'app/shared/reducers';
import {getPhotos} from 'app/shared/reducers/album';

interface IAlbumView extends StateProps, DispatchProps {
	match: {}
}

export const AlbumView = (props: IAlbumView) => {
	return (
		<div>{props.match.params.id}</div>
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
