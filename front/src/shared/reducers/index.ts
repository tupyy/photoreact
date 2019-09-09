import { combineReducers } from 'redux';
import { loadingBarReducer as loadingBar } from 'react-redux-loading-bar';

import locale, { LocaleState } from './locale';
import authentication, { AuthenticationState } from './authentication';
import album, {AlbumState} from './album';
import navbar, {NavBarState} from './navbar';

export interface IRootState {
  readonly authentication: AuthenticationState;
  readonly locale: LocaleState;
  readonly loadingBar: any;
  readonly album: AlbumState
  readonly navbar: NavBarState
}

const rootReducer = combineReducers<IRootState>({
  authentication,
  locale,
  loadingBar,
  album,
  navbar
});

export default rootReducer;
