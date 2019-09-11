import {makeStyles, createStyles} from '@material-ui/core';
import {Theme} from "@material-ui/core/styles/createMuiTheme";

const useStyles = makeStyles((theme:Theme) => {
    createStyles({
        userName: {
            paddingLeft: '16px',
            paddingRight: '16px',
            paddingTop: '4px',
            paddingBottom: '4px'
        }
    })
});

export default useStyles;