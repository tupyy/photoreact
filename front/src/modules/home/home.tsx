import './home.scss';

import React from 'react';
import {connect} from 'react-redux';
import MediaContainer from 'app/shared/components/container/media-container';

export type IHomeProp = StateProps;

export const Home = (props: IHomeProp) => {
  const { account } = props;

  return (
      <div>
        Home
        <MediaContainer></MediaContainer>
      </div>
  )
};

const mapStateToProps = storeState => ({
  account: storeState.authentication.account,
  isAuthenticated: storeState.authentication.isAuthenticated
});

type StateProps = ReturnType<typeof mapStateToProps>;

export default connect(mapStateToProps)(Home);
