import React, {useState, useEffect} from 'react';
import {Avatar, Popover, makeStyles, Theme, Typography} from '@material-ui/core';
import {getNameInitials} from "app/shared/util/user-name-utils";
import useHover from 'app/shared/hook/use-hover';

interface IUserAvatar {
    firstName: string;
    lastName: string;
    profilePhoto?: string
    size?: string
}

const useStyles = makeStyles((theme:Theme) =>({
    photo: {
        width: '100%'
    },
    bigAvatar: {
        marginRight: 'auto',
        marginLeft: 'auto',
        margin: 10,
        width: 90,
        height: 90,
        [theme.breakpoints.up("sm")]: {
            fontSize: '2.5rem'
        },
        [theme.breakpoints.only("xs")]: {
            fontSize: '1.5rem',
            width: 50,
            height: 50
        }
    },
}));

const UserAvatar = (props: IUserAvatar) => {
    const [imgError, setImgError] = useState(false);
	const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);

	function handlePopoverOpen(event: React.MouseEvent<HTMLElement, MouseEvent>) {
		setAnchorEl(event.currentTarget);
	}

	function handlePopoverClose() {
		setAnchorEl(null);
	}

	const open = Boolean(anchorEl);

	const renderPopover = (classes: {}) => {
		return (
		<Popover
			id="avatar-popover"
			className={classes.popover}
			classes={{
				paper: classes.paper,
			}}
			open={open}
			anchorEl={anchorEl}
			anchorOrigin={{
				vertical: 'bottom',
				horizontal: 'left',
			}}
			transformOrigin={{
				vertical: 'top',
				horizontal: 'left'
			}}
			onClose={handlePopoverClose}
			disableResponseFocus
		>
		<Typography>Popover</Typography>
		</Popover>
	)}

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
			<div>
				<div onMouseEnter={handlePopoverOpen}>
					<Avatar 
						className={props.size === 'xl' ? classes.bigAvatar : null}
					>
						{getNameInitials(props.firstName, props.lastName)}
					</Avatar>
				</div>
				{renderPopover(classes)}
			</div>
        )
    }
}

export default UserAvatar;
