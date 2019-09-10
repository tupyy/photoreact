import { string } from "prop-types";
import { async } from "q";

export const ACTION_TYPES = {
    SHOW_NAV_BAR: 'navbar/SHOW_NAV_BAR',
    HIDE_NAV_BAR: 'navbar/HIDE_NAV_BAR',
    SET_USER_DATA: 'navbar/SET_USER_DATA'
}

const initialState = {
    visible: true,
    userProfile: {} as any 
}

export type NavBarState = Readonly<typeof initialState>

export default (state: NavBarState = initialState, action) : NavBarState {
    switch(action.type) {
        case ACTION_TYPES.SHOW_NAV_BAR:
            return {
                ...state,
                visible: true
            };
        case ACTION_TYPES.HIDE_NAV_BAR:
            return {
                ...state,
                visible: false
            };
        case ACTION_TYPES.SET_USER_DATA:
            return {
                ...state,
                userProfile: action.data
            }
        default:
            return state;
    }
}

export const setUserProfile = userData => dispatch => {
    dispatch({
        type: ACTION_TYPES.SET_USER_DATA,
        data: userData
    })
};

export const showNavBar = () => (dispatch) => {
    dispatch({
        type:ACTION_TYPES.SHOW_NAV_BAR
    });
}

export const hideNavBar = () => (dispatch) => {
    dispatch({
        type:ACTION_TYPES.HIDE_NAV_BAR)
    };
};
