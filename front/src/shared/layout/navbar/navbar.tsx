import { AppBar, IconButton, Toolbar, Typography } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import MoreIcon from '@material-ui/icons/MoreVert';
import { IRootState } from 'app/shared/reducers';
import React from 'react';
import { connect } from 'react-redux';
import NavBarNotifications from './navbar-notifications';
import useStyles from './navbar-styles';
import UserMenu from './user-menu';

export interface INavBarProps extends StateProps {};

const NavBar = (props: INavBarProps) => {
    const classes = useStyles();
  
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
              <NavBarNotifications />
              <UserMenu userProfile={props.userProfile} sectionType="desktop" />
            </div>
            <div className={classes.sectionMobile}>
              <UserMenu userProfile={props.userProfile} sectionType="mobile" />
            </div>
          </Toolbar>
        </AppBar>
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
