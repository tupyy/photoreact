import {FAILURE, REQUEST, SUCCESS} from 'app/shared/reducers/action-type.util';
import axios from 'axios';

export const ACTION_TYPES = {
    GET_RECENT_ALBUMS : 'media/GET_RECENT_ALBUMS'
}

const initialState = {
    loading: false,
    errorMessage: null as string,
    album: null,
    recentAlbums: []
}

export type AlbumsState = Readonly<typeof initialState>;

export default (state: AlbumsState = initialState, action) : AlbumsState => {
    switch(action.type) {
        case REQUEST(ACTION_TYPES.GET_RECENT_ALBUMS):
            return {
                ...state,
                loading: true
            };
        case FAILURE(ACTION_TYPES.GET_RECENT_ALBUMS):
            return {
                ...initialState,
                errorMessage: action.payload
            };
        case SUCCESS(ACTION_TYPES.GET_RECENT_ALBUMS):
            return {
                ...state,
                loading: false,
                recentAlbums: action.payload.data.albums
            }
        default:
            return state;
    }
}    


export const getRecentAlbums = () => async (dispatch) => {
    await dispatch({
        type: ACTION_TYPES.GET_RECENT_ALBUMS,
        payload: axios.get('api/albums?limit=5')
    });
}
