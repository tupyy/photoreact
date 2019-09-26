import {makeStyles, Theme, createStyles, createMuiTheme} from '@material-ui/core';
import {red} from '@material-ui/core/colors'

export const theme = createMuiTheme({
	typography: {
		fontFamily: [
			'Ubuntu',
			'Lato',
			'Roboto',
			'sans-serif',
		].join(','),
	},
});

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    card: {
      maxWidth: 230,
    },
    media: {
		width: '100%',
		cursor: 'pointer'
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
	link: {
		fontFamily: 'Roboto sans-serif',
		cursor: "pointer"
	},
	description: {
		fontFamily: 'Ubuntu Regular sans-serif',
	}
  }),
);

export default useStyles;
