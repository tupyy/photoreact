import React, {useState} from 'react';
import Photo from 'app/shared/components/photo/photo';
import { Avatar } from '@material-ui/core';
import { makeStyles, createStyles } from '@material-ui/core';
import { red } from '@material-ui/core/colors';

interface IUserAvatar {
  firstName: string;
  lastName: string;
  profilePhoto?: string
}

const capitalize = (str: string): string => {
  if (str) {
    return str.charAt(0).toUpperCase + str.slice(1);
  }
  return '';
};


const getFullName = (firstName: string, lastName: string): string => {
  return capitalize(firstName) + " " + capitalize(lastName);
};

const getAvatarName = (firstName: string, lastName: string): string => {
  if (firstName && lastName) {
    return firstName.charAt(0).toUpperCase().concat(lastName.charAt(0).toUpperCase());
  }
  return "";
};

const useStyles = makeStyles({
  photo: {
    width: '100%'
  },
  avatar: {
    backgroundColor: red[500],
  }
});

const UserAvatar = (props: IUserAvatar) => {
  const [imgError, setImgError] = useState(false);

  // @ts-ignore
  const classes = useStyles();

  if (props.profilePhoto && !imgError) {
    return (
      <Avatar
        className={classes.avatar}
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
        {getAvatarName(props.firstName, props.lastName)}
      </Avatar>
    )
  }
}

export default UserAvatar;
