import {makeStyles, createStyles} from '@material-ui/core';
import {Theme} from '@material-ui/core/';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
        flewGrow: 1,
    },
    paper: {
        width: '100%'
    },
  }),
);

export default useStyles;