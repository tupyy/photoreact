export const ACTION_TYPES = {
    SHOW_NAV_BAR: 'header/SHOW_NAV_BAR',
    HIDE_NAV_BAR: 'header/HIDE_NAV_BAR'
}

const initialState = {
    visible: true
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
        default:
            return state;
    }
}

export const showNavBar = () => (dispatch) => {
    dispatch({
        type:ACTION_TYPES.SHOW_NAV_BAR
    });
}

export const hideNavBar = () => (dispatch) => {
    dispatch({
        type:ACTION_TYPES.HIDE_NAV_BAR)
    };
}
