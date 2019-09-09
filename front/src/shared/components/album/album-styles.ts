import {makeStyles, Theme, createStyles} from '@material-ui/core';
import {red} from '@material-ui/core/colors'

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    card: {
      maxWidth: 230,
    },
    media: {
      width: '100%'
    },
    expand: {
      transform: 'rotate(0deg)',
      marginLeft: 'auto',
      transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
      }),
    },
    expandOpen: {
      transform: 'rotate(180deg)',
    },
    cardActions: {
      display: 'flex',
      justifyContent: 'center'
    },
    avatar: {
      backgroundColor: red[500],
    },
  }),
);

export default useStyles;