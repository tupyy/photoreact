import './home.scss';

import React, { useEffect } from 'react';
import {connect} from 'react-redux';
import MediaContainer from 'app/shared/components/container/media-container';
import { IRootState } from 'app/shared/reducers';
import {showNavBar} from 'app/shared/reducers/navbar';

export interface IHomeProp extends StateProps, DispatchProps {};

export const Home = (props: IHomeProp) => {
  const { account } = props;
  
  useEffect( () => {
    props.showNavBar();
  }, [])

  return (
      <div>
        Home
        <MediaContainer></MediaContainer>
      </div>
  )
};

const mapStateToProps = ({authentication}: IRootState) => ({
  account: authentication.account,
  isAuthenticated: authentication.isAuthenticated
});

const mapDispatchToProps = {
  showNavBar
}

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Home);
