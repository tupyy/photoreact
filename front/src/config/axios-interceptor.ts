import axios from 'axios';
import { Storage } from '../utils';
import { SERVER_API_URL } from './constants';


const TIMEOUT = 1 * 60 * 1000;
const AMAZON_AWS_PATTERN = "amazonaws";

axios.defaults.timeout = TIMEOUT;
axios.defaults.baseURL = SERVER_API_URL;

const setupAxiosInterceptors = (onUnauthenticated: any) => {
    const onRequestSuccess = (config : any) => {
        const token = Storage.local.get('pr-authenticationToken') || Storage.session.get('pr-authenticationToken');
        if (token && isLocalRequest(config.url)) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    };
    const onResponseSuccess = (response: any) => response;
    const onResponseError = (err: any) => {
        const status = err.status || (err.response ? err.response.status : 0);
        if (status === 403 || status === 401) {
            onUnauthenticated();
        }
        return Promise.reject(err);
    };
    axios.interceptors.request.use(onRequestSuccess);
    axios.interceptors.response.use(onResponseSuccess, onResponseError);
};

const isLocalRequest = (url: string) => {
    return url.indexOf(AMAZON_AWS_PATTERN) === -1
};
export default setupAxiosInterceptors;
