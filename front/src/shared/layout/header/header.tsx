import NavBar from 'app/shared/layout/navbar/navbar';
import React from 'react';
import LoadingBar from 'react-redux-loading-bar';
import {IRootState} from 'app/shared/reducers';
import { connect } from 'react-redux';

export interface IHeaderProps {
  isAuthenticated: boolean;
  isAdmin: boolean;
  showNavBar: boolean
}

export interface IHeaderState {
  menuOpen: boolean;
}

const Header = (props: IHeaderProps) => {
  
  return (
    <div id="app-header">
      {props.showNavBar ?  (
        <div>
          <LoadingBar className="loading-bar" />
          <NavBar /> 
        </div>
          ) : null
      }
    </div>
  );
}

const mapStateToProps = ({navbar} : IRootState) => ({
  showNavBar: navbar.visible
})

type StateProps = ReturnType<typeof mapStateToProps>

export default connect(
  mapStateToProps
)(Header);
