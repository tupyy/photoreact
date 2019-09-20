import {timedelta} from 'app/shared/util/date-utils';
import moment from 'moment';

const config = {
  VERSION: process.env.VERSION
};

export default config;

export const SERVER_API_URL = process.env.SERVER_API_URL;

export const AUTHORITIES = {
  ADMIN: 'admin',
  USER: 'user'
};

export const messages = {
  DATA_ERROR_ALERT: 'Internal Error'
};

export const APP_DATE_FORMAT = 'DD/MM/YY HH:mm';
export const APP_TIMESTAMP_FORMAT = 'DD/MM/YY HH:mm:ss';
export const APP_LOCAL_DATE_FORMAT = 'DD/MM/YYYY';
export const APP_LOCAL_DATETIME_FORMAT = 'DD-MM-YYYY';
export const APP_LOCAL_DATETIME_FORMAT_2 = 'YYYY-MM-DD';
export const APP_LOCAL_DATETIME_FORMAT_Z = 'YYYY-MM-DDTHH:mm Z';
export const APP_WHOLE_NUMBER_FORMAT = '0,0';
export const APP_TWO_DIGITS_AFTER_POINT_NUMBER_FORMAT = '0,0.[00]';

// Export URL API
export const API_USER_PROFILE_ACTIVITIES = "api/activity/?activity_from=" +timedelta(-7) + '&activity_to=' + moment().format(APP_LOCAL_DATETIME_FORMAT_2) + "&ordering=date";
export const API_USER_PROFILE_ALBUMS = "api/albums/?limit=5";
export const API_USER_PROFILE_PERMISSION_LOG = "api/permission/log/?log_from=" + timedelta(-7) + '&log_to=' + moment().format(APP_LOCAL_DATETIME_FORMAT_2);
