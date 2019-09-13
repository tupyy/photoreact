import {makeStyles, Theme} from "@material-ui/core";

/**
 * Defines common styles for all tab components
 */
const useTabComponentStyles = makeStyles( (theme: Theme) => ({
    hidden: {
        display: 'none'
    },
    root: {
        display: 'block'
    }
}));

export default useTabComponentStyles;
