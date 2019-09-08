import { combineReducers } from 'redux';
import { loadingBarReducer as loadingBar } from 'react-redux-loading-bar';

import locale, { LocaleState } from './locale';
import authentication, { AuthenticationState } from './authentication';
import media, {MediaState} from './media';

export interface IRootState {
  readonly authentication: AuthenticationState;
  readonly locale: LocaleState;
  readonly loadingBar: any;
  readonly media: MediaState
}

const rootReducer = combineReducers<IRootState>({
  authentication,
  locale,
  loadingBar,
  media
});

export default rootReducer;
