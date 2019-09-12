import React, {useState} from 'react';
import Photo from 'app/shared/components/photo/photo';
import { Avatar } from '@material-ui/core';
import { makeStyles, createStyles } from '@material-ui/core';
import { red } from '@material-ui/core/colors';
import {getNameInitials} from "app/shared/util/user-name-utils";

interface IUserAvatar {
  firstName: string;
  lastName: string;
  profilePhoto?: string
  size?: string
}

const useStyles = makeStyles({
  photo: {
    width: '100%'
  },
  bigAvatar: {
    margin: 10,
    width: 120,
    height: 120,
  },
});

const UserAvatar = (props: IUserAvatar) => {
  const [imgError, setImgError] = useState(false);

  // @ts-ignore
  const classes = useStyles();

  if (props.profilePhoto && !imgError) {
    return (
      <Avatar
        className={props.size === 'xl' ? classes.bigAvatar : null}
        src={props.profilePhoto}
        imgProps={
          { "onError": () => {setImgError(true)} }
        }
      >
      </Avatar>
    )
  } else {
    return (
      <Avatar>
        {getNameInitials(props.firstName, props.lastName)}
      </Avatar>
    )
  }
}

export default UserAvatar;
