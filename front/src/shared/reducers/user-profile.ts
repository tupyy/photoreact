import { FAILURE, REQUEST, SUCCESS } from 'app/shared/reducers/action-type.util';
import {IAlbum} from 'app/shared/model/album.model';
import {IPermissionLog} from 'app/shared/model/permission_log.model';
import {getPermissionLogMockingData} from 'app/shared/model/permission_log.model';
import {IActivity} from 'app/shared/model/activity.model';
import axios from 'axios';
import {API_USER_PROFILE_ALBUMS, API_USER_PROFILE_ACTIVITIES, API_USER_PROFILE_PERMISSION_LOG} from 'app/config/constants';

export const ACTION_TYPES = {
	GET_USER_ALBUMS: 'userProfile/GET_USER_ALBUMS',
	GET_USER_ACTIVITY: 'userProfile/GET_USER_ACTIVITY',
 	GET_USER_PERMISSION_LOG: 'userProfile/GET_USER_PERMISSION_LOG'
};

const initialState = {
	loading: false,
	albums: [] as IAlbum[],
	activities: [] as IActivity[],
	errorMessage: null as string,
	permissionLogs: [] as IPermissionLog[]
}


export type UserProfileState = Readonly<typeof initialState>;

export default (state: UserProfileState = initialState, action): UserProfileState => {
	switch(action.type) {
		case REQUEST(ACTION_TYPES.GET_USER_PERMISSION_LOG):
		case REQUEST(ACTION_TYPES.GET_USER_ALBUMS):
		case REQUEST(ACTION_TYPES.GET_USER_ACTIVITY):
			return {
				...state,
				loading: true
		};
		case FAILURE(ACTION_TYPES.GET_USER_PERMISSION_LOG):
		case FAILURE(ACTION_TYPES.GET_USER_ALBUMS):
		case FAILURE(ACTION_TYPES.GET_USER_ACTIVITY):
			return {
				...state,
				loading: false,
				errorMessage: action.payload
		};
		case SUCCESS(ACTION_TYPES.GET_USER_ALBUMS):
		   return {
				...state,
				loading: false,
				albums: action.payload.data.albums
		};
		case SUCCESS(ACTION_TYPES.GET_USER_ACTIVITY):
			return {
				...state,
				loading: false,
				activities: action.payload.data.results
		};
		case SUCCESS(ACTION_TYPES.GET_USER_PERMISSION_LOG):
			return {
				...state,
				loading: false,
				permissionLogs: action.payload.data.logs
		};
		default:
			return state
	};
};

export const getAlbums = () => async (dispatch) => {
	await dispatch({
		type: ACTION_TYPES.GET_USER_ALBUMS,
		payload: axios.get(API_USER_PROFILE_ALBUMS)
	});
};

export const getActivities = () => async (dispatch) => {
	await dispatch({
		type: ACTION_TYPES.GET_USER_ACTIVITY,
		payload: axios.get(API_USER_PROFILE_ACTIVITIES)
	});
};

export const getPermissionLogs = () => async (dispatch) => {
	await dispatch({
		type: ACTION_TYPES.GET_USER_PERMISSION_LOG,
		payload: axios.get(API_USER_PROFILE_PERMISSION_LOG)
	});
};


/**
 * Temporary mocking service for permission log API
 */
const getPermissionLogData = () : Promise<IPermissionLog[]> => {
	return new Promise( (resolve, reject) => {
		resolve(getPermissionLogMockingData());
	});
};
