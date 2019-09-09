import React from 'react';
import Photo from 'app/shared/components/photo/photo';
import {Avatar} from '@material-ui/core';
import {makeStyles, createStyles} from '@material-ui/core';
import {red} from '@material-ui/core/colors';

interface IUserAvatar {
    firstName: string;
    lastName: string;
    profilePhoto?: string
}

function capitalize(str: string): string {
    return str.charAt(0).toUpperCase + str.slice(1);
}

function getFullName(firstName: string, lastName: string): string {
    return capitalize(firstName) + " " + capitalize(lastName);
}

function getAvarName(firstName: string, lastName: string) : string {
    return firstName.charAt(0).toUpperCase + lastName.charAt(0).toUpperCase;
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    photo: {
      width: '100%'
    },
    avatar: {
      backgroundColor: red[500],
    },
  }),
);

const UserAvatar = (props: IUserAvatar) => {
   const classes = useStyles()

   if (props.profilePhoto) {
       return (
            <Avatar 
                className={classes.avatar}    
                src={props.profilePhoto} 
                alt={getFullName(props.firstName, props.lastName)} />
       )
   } else {
       return (
            <Avatar>
                {getAvarName(props.firstName, props.lastName)}
            </Avatar>
        )
   }
}

export default UserAvatar;