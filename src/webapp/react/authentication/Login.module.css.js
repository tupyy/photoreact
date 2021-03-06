import Image from "../../../../public/login_photo.jpg";

const styles = theme => ({
    root: {
        height: '100vh',
    },
    image: {
        backgroundImage: `url(${Image})`,
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    },
    paper: {
        margin: theme.spacing(8, 4),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing(1),
    },
    buttonContainer: {
        position: 'relative',
        width: '100%',
        height: '50px'
    },
    submit: {
        // margin: theme.spacing(3, 0, 2),
        position: 'absolute',
        top: '0',
        left: '0',
    },
    progress : {
      position: 'absolute',
      top: '0',
      left: '45%',
        width: '100%',
        height: '100%'
    },
    loginFailed: {
        color: 'red',
        fontWeight: 'bold'
    }
});

export default styles;
