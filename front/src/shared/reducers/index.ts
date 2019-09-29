import { combineReducers } from 'redux';
import { loadingBarReducer as loadingBar } from 'react-redux-loading-bar';

import locale, { LocaleState } from './locale';
import authentication, { AuthenticationState } from './authentication';
import albums, {AlbumsState} from './albums';
import navbar, {NavBarState} from './navbar';
import userProfile, {UserProfileState} from './user-profile';

export interface IRootState {
  readonly authentication: AuthenticationState;
  readonly locale: LocaleState;
  readonly loadingBar: any;
  readonly albums: AlbumsState;
  readonly navbar: NavBarState;
  readonly userProfile: UserProfileState;
}

const rootReducer = combineReducers<IRootState>({
  authentication,
  locale,
  loadingBar,
  albums,
  navbar,
  userProfile
});

export default rootReducer;
