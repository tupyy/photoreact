import './home.scss';

import React, { useEffect } from 'react';
import {connect} from 'react-redux';
import MediaContainer from 'app/shared/components/container/media-container';
import Album from 'app/shared/components/album/album';
import { IRootState } from 'app/shared/reducers';
import {showNavBar} from 'app/shared/reducers/navbar';
import {getRecentAlbums} from 'app/shared/reducers/albums';


export interface IHomeProp extends StateProps, DispatchProps {};

export const Home = (props: IHomeProp) => {
  const { account } = props;
  
  useEffect( () => {
    props.showNavBar();
	props.getRecentAlbums();
  }, [])

  return (
      <div>
        Home
		<MediaContainer
			component={Album}
			data={props.recentAlbums}
		></MediaContainer>
      </div>
  )
};

const mapStateToProps = ({authentication, albums}: IRootState) => ({
  account: authentication.account,
	isAuthenticated: authentication.isAuthenticated,
	recentAlbums: albums.recentAlbums
});

const mapDispatchToProps = {
	showNavBar,
	getRecentAlbums
}

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Home);
