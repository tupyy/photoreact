import React from 'react';
import {Typography} from "@material-ui/core";

interface IUserProfileHeader {
    // component to show user avatar
    avatarComponent: any,
    title: string
}

/**
 * this component shows the header of the user profile page.
 */
const UserProfileHeader = (props: IUserProfileHeader) => {
  return (
      <div>
          {props.avatarComponent}
          <Typography variant="h5">{props.title}</Typography>
      </div>
  )
};

export default UserProfileHeader;
