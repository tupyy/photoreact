import React from 'react';
import {Container, makeStyles, Typography} from "@material-ui/core";

interface IUserProfileHeader {
    // component to show user avatar
    avatarComponent: any,
    title: string
}

const useStyles = makeStyles({
    root: {
        display: 'flex',
        justifyContent: 'center',
        marginLeft: 0,
        marginRight: 0,
        padding: 0,
        background: '#fafafa'

    },
    secondary: {
        display: 'block'
    },
    title: {
        fontSize: '23px'
    }
});

/**
 * this component shows the header of the user profile page.
 */
const UserProfileHeader = (props: IUserProfileHeader) => {

    const classes = useStyles();
    return (
        <Container className={classes.root}>
            <div className={class.secondary}>
                {props.avatarComponent}
                <Typography variant="h6" className={classes.title}>{props.title}</Typography>
            </div>
        </Container>
    )
};

export default UserProfileHeader;
