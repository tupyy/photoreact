import {FAILURE, REQUEST, SUCCESS} from 'app/shared/reducers/action-type.util';
import {IPhoto} from 'app/shared/model/photo';
import axios from 'axios';

export const ACTION_TYPES = {
    GET_PHOTOS : 'album/GET_PHOTOS',
	CHANGE_MODE: 'album/CHANGE_MODE'
}

export const MODE_TYPES = {
	VIEW_MODE : 'viewMode',
	EDIT_MODE: 'editMode'
}

const initialState = {
    loading: false,
    errorMessage: null as string,
    album: null,
	photos: null as IPhoto[],
	mode: MODE_TYPES.VIEW_MODE,
	selectedPhotos: null as IPhoto[]
}

export type AlbumState = Readonly<typeof initialState>;

export default (state: AlbumState = initialState, action) : AlbumState => {
    switch(action.type) {
        case REQUEST(ACTION_TYPES.GET_PHOTOS):
            return {
                ...state,
                loading: true
            };
        case FAILURE(ACTION_TYPES.GET_PHOTOS):
            return {
                ...initialState,
                errorMessage: action.payload
            };
        case SUCCESS(ACTION_TYPES.GET_PHOTOS):
            return {
                ...state,
                loading: false,
                photos: action.payload.data
            }
        default:
            return state;
    }
}    


export const getPhotos = (id:string) => async (dispatch) => {
    await dispatch({
        type: ACTION_TYPES.GET_PHOTOS,
        payload: axios.get('api/photos/' + id + '/')
    });
}
