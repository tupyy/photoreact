import React from 'react';
import {Menu, MenuItem} from '@material-ui/core';
import NavBarNotifications from './navbar-notifications';
import UserAvatar from 'app/shared/components/user_avatar/user-avatar';
import {IconButton} from '@material-ui/core';
import MoreIcon from '@material-ui/icons/MoreVert';

export interface IUserMenuProps {
    userProfile : {},
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
  
    const menuId = 'primary-search-account-menu';
    const renderMenu = (
      <Menu
        anchorEl={anchorEl}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        id={menuId}
        keepMounted
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        open={isMenuOpen}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
        <MenuItem onClick={handleMenuClose}>My account</MenuItem>
      </Menu>
    );
  
    const mobileMenuId = 'primary-search-account-menu-mobile';
    const renderMobileMenu = (
      <Menu
        anchorEl={mobileMoreAnchorEl}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        id={mobileMenuId}
        keepMounted
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        open={isMobileMenuOpen}
        onClose={handleMobileMenuClose}
      >
        <MenuItem>
          <NavBarNotifications />
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
                      <MoreIcon />
                    </IconButton>
            )
            }
        {renderMobileMenu}
        {renderMenu}
        </div>
    )
}

export default UserMenu;