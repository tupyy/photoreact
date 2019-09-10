import React from 'react';
import useStyles from './navbar-styles';
import {
    Menu, 
    MenuItem, 
    IconButton, 
    Badge,
    AppBar,
    Toolbar,
    Typography
} from '@material-ui/core';
import NotificationsIcon from '@material-ui/icons/Notifications';
import MenuIcon from '@material-ui/icons/Menu';
import AccountCircle from '@material-ui/icons/AccountCircle';
import MoreIcon from '@material-ui/icons/MoreVert';
import { IRootState } from 'app/shared/reducers';
import { connect } from 'react-redux';
import UserAvatar from 'app/shared/components/user_avatar/user-avatar';
import { checkPropTypes } from 'prop-types';

export interface INavBarProps extends StateProps {};

const NavBar = (props: INavBarProps) => {
    const classes = useStyles();
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
          <IconButton aria-label="show 11 new notifications" color="inherit">
            <Badge badgeContent={11} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>
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
      <div className={classes.grow}>
        <AppBar position="static">
          <Toolbar>
            <IconButton
              edge="start"
              className={classes.menuButton}
              color="inherit"
              aria-label="open drawer"
            >
              <MenuIcon />
            </IconButton>
            <Typography className={classes.title} variant="h6" noWrap>
              Photos
            </Typography>
            <div className={classes.grow} />
            <div className={classes.sectionDesktop}>
              <IconButton aria-label="show 17 new notifications" color="inherit">
                <Badge badgeContent={17} color="secondary">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
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
            </div>
            <div className={classes.sectionMobile}>
              <IconButton
                aria-label="show more"
                aria-controls={mobileMenuId}
                aria-haspopup="true"
                onClick={handleMobileMenuOpen}
                color="inherit"
              >
                <MoreIcon />
              </IconButton>
            </div>
          </Toolbar>
        </AppBar>
        {renderMobileMenu}
        {renderMenu}
      </div>
    );
  }

const mapStateToProps = ({navbar}: IRootState) => ({
    userProfile: navbar.userProfile
});

type StateProps = ReturnType<typeof mapStateToProps>

export default connect(
    mapStateToProps
)(NavBar);
