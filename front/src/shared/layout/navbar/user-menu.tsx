import React from 'react';
import {Menu, MenuItem, Divider, Typography} from '@material-ui/core';
import NavBarNotifications from './navbar-notifications';
import UserAvatar from 'app/shared/components/user_avatar/user-avatar';
import {IconButton} from '@material-ui/core';
import MoreIcon from '@material-ui/icons/MoreVert';
import useStyles from './user-menu-styles';

export interface IUserMenuProps {
    userProfile: {},
    sectionType: string
}

const UserMenu = (props: IUserMenuProps) => {
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = React.useState<null | HTMLElement>(null);

    const isMenuOpen = Boolean(anchorEl);
    const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);

    function handleProfileMenuOpen(event: React.MouseEvent<HTMLElement>) {
        setAnchorEl(event.currentTarget);
    }

    function handleMobileMenuClose() {
        setMobileMoreAnchorEl(null);
    }

    function handleMenuClose() {
        setAnchorEl(null);
        handleMobileMenuClose();
    }

    function handleMobileMenuOpen(event: React.MouseEvent<HTMLElement>) {
        setMobileMoreAnchorEl(event.currentTarget);
    }

    const getFullName = (firstName: string, lastName: string): string => {
        if (firstName && lastName) {
            return firstName.charAt(0).toUpperCase() + firstName.slice(1) +
                ' ' + lastName.charAt(0).toUpperCase() + lastName.slice(1);
        }
        return '';
    };

    const menuId = 'primary-search-account-menu';
    const classes = useStyles();

    const renderMenu = (
        <Menu
            anchorEl={anchorEl}
            getContentAnchorEl={null}
            anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
            id={menuId}
            keepMounted
            transformOrigin={{vertical: 'top', horizontal: 'right'}}
            open={isMenuOpen}
            onClose={handleMenuClose}
        >
            <Typography
                className={classes.username}>{getFullName(props.userProfile.first_name, props.userProfile.last_name)}</Typography>
            <Divider orientation="horizontal"/>
            <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
            <MenuItem onClick={handleMenuClose}>My account</MenuItem>
            <Divider orientation="horizontal"/>
            <MenuItem>Logout</MenuItem>
        </Menu>
    );

    const mobileMenuId = 'primary-search-account-menu-mobile';
    const renderMobileMenu = (
        <Menu
            anchorEl={mobileMoreAnchorEl}
            getContentAnchorEl={null}
            anchorOrigin={{vertical: 'bottom', horizontal: 'right'}}
            id={mobileMenuId}
            keepMounted
            transformOrigin={{vertical: 'top', horizontal: 'right'}}
            open={isMobileMenuOpen}
            onClose={handleMobileMenuClose}
        >
            <MenuItem>
                <NavBarNotifications/>
                <p>Notifications</p>
            </MenuItem>
            <MenuItem onClick={handleProfileMenuOpen}>
                <IconButton
                    aria-label="account of current user"
                    aria-controls="primary-search-account-menu"
                    aria-haspopup="true"
                    color="inherit"
                >
                    <UserAvatar
                        firstName={props.userProfile.first_name}
                        lastName={props.userProfile.last_name}
                        profilePhoto={props.userProfile.photo}
                    />
                </IconButton>
                <p>Account</p>
            </MenuItem>
        </Menu>
    );

    return (
        <div>
            {props.sectionType === "desktop" ? (
                <IconButton
                    edge="end"
                    aria-label="account of current user"
                    aria-controls={menuId}
                    aria-haspopup="true"
                    onClick={handleProfileMenuOpen}
                    color="inherit"
                >
                    <UserAvatar
                        firstName={props.userProfile.first_name}
                        lastName={props.userProfile.last_name}
                        profilePhoto={props.userProfile.photo}
                    />
                </IconButton>
            ) : (
                <IconButton
                    edge="end"
                    aria-label="account of current user"
                    aria-controls={mobileMenuId}
                    aria-haspopup="true"
                    onClick={handleMobileMenuOpen}
                    color="inherit"
                >
                    <MoreIcon/>
                </IconButton>
            )
            }
            {renderMobileMenu}
            {renderMenu}
        </div>
    )
}

export default UserMenu;
