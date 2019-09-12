import React, {useState} from 'react';
import {Avatar, makeStyles} from '@material-ui/core';
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
        display: 'block',
        marginRight: 'auto',
        marginLeft: 'auto',
        margin: 10,
        width: 90,
        height: 90,
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
                    {
                        "onError": () => {
                            setImgError(true)
                        }
                    }
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
