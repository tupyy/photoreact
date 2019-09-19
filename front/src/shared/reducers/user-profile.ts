import { FAILURE, REQUEST, SUCCESS } from 'app/shared/reducers/action-type.util';
import {IAlbum} from 'app/shared/model/album.model';
import {IPermissionLog} from 'app/shared/model/permission_log.model';
import {getPermissionLogMockingData} from 'app/shared/model/permission_log.model';
import {IActivity} from 'app/shared/model/activity.model';
import axios from 'axios';
import {timedelta} from 'app/shared/util/date-utils';
import {APP_LOCAL_DATETIME_FORMAT_2} from 'app/config/constants';
import moment from 'moment';

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
	permissionLog: [] as IPermissionLog[]
}

const URL_ACTIVITIES = "api/activity?activity_from=" +timedelta(-7) + '&activity_to=' + moment().format(APP_LOCAL_DATETIME_FORMAT_2) + "&ordering=date";
const URL_ALBUMS = "api/albums?limit=5";
const URL_PERMISSION_LOG = "api/permission/log?permission_from=" + timedelta(-7) + '&permission_to=' + moment().format(APP_LOCAL_DATETIME_FORMAT_2) + "&ordering=date";

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
				permissionLog: action.payload
		};
		default:
			return state
	};
};

export const getAlbums = () => async (dispatch) => {
	await dispatch({
		type: ACTION_TYPES.GET_USER_ALBUMS,
		payload: axios.get(URL_ALBUMS)
	});
};

export const getActivities = () => async (dispatch) => {
	await dispatch({
		type: ACTION_TYPES.GET_USER_ACTIVITY,
		payload: axios.get(URL_ACTIVITIES)
	});
};

export const getPermissionLogs = () => async (dispatch) => {
	await dispatch({
		type: ACTION_TYPES.GET_USER_PERMISSION_LOG,
		payload: getPermissionLogData()
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
