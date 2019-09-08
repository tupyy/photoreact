import React, {useState} from 'react';
import {Container, CssBaseline, Link} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Avatar from "@material-ui/core/Avatar";
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import TextField from "@material-ui/core/TextField";
import Checkbox from "@material-ui/core/Checkbox";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import useStyles from "./login-form-style";

export interface ILoginModalProps {
    loginError: boolean;
    handleLogin: Function;
}

function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            Cosmin Tupangiu
            {' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

const LoginForm = (props: ILoginModalProps) => {
    const [username, setUsername] = useState('cosmin');
    const [password, setPassword] = useState('cosmin');
    const [rememberMe, setRememberMe] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        const {handleLogin} = props;
        handleLogin(username, password, rememberMe)
    };

    const handleChange = (event: any) => {
        const method = event.target.name === "username" ? setUsername : setPassword;
        method(event.target.value);
    };

    const classes = useStyles();
    const loginError = props.loginError;
    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <div className={classes.paper}>
                <Avatar className={classes.avatar}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign in
                </Typography>
                <form className={classes.form} noValidate onSubmit={handleSubmit}>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                        value={username}
                        onChange={handleChange}
                        autoFocus
                    />
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        value={password}
                        onChange={handleChange}
                        autoComplete="current-password"
                    />
                    <FormControlLabel
                        control={
                            <Checkbox 
                                checked={rememberMe}
                                onClick={() => setRememberMe(!rememberMe)} 
                                color="primary" 
                            />}
                        label="Remember me"
                    />
                    {loginError && 
                        <Typography component="h5">
                            Login failed
                        </Typography>
                    }
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                    >
                        Sign In
                    </Button>
                    <Grid container>
                        <Grid item xs>
                            <Link href="#" variant="body2">
                                Forgot password?
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
            <Box mt={8}>
                <Copyright />
            </Box>
        </Container>
    );
};

export default LoginForm;

