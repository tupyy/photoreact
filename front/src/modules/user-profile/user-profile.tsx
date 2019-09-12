import React from 'react';
import {connect} from 'react-redux';
import {IRootState} from "app/shared/reducers";

interface IUserProfileProps extends StateProps {

}

/**
 * Main component to show the user profile.
 */
const UserProfile = (props: IUserProfileProps) => {
  return (
      <div>UserProfile</div>
  )
};

const mapStateToProps = ( {authentication} : IRootState) => ({
  account: authentication.account
});

type StateProps = ReturnType<typeof mapStateToProps>;

export default connect(
    mapStateToProps
)(UserProfile)
