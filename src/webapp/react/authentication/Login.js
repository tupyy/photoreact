import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import styles from './Login.module.css';
import {withStyles} from "@material-ui/core";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faUser} from '@fortawesome/free-solid-svg-icons';
import Container from "@material-ui/core/Container";
import {authenticate} from "../../redux/reducers/authenticationReducer";
import {connect} from "react-redux";
import {withRouter} from "react-router";
import CircularProgress from "@material-ui/core/CircularProgress";

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email: "",
            password: "",
            loginRequested: false,
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    validateForm() {
        return this.state.email.length > 0 && this.state.password.length > 0;
    }

    handleChange(event) {
        this.setState({
            [event.target.id]: event.target.value
        })
    }

    handleSubmit(event) {
        event.preventDefault();
        this.setState({
            loginRequested: true
        });
        this.props.authenticate(this.state.email, this.state.password);
    };

    componentWillReceiveProps(nextProps, nextContext) {
        if (nextProps.authentication.userAuthenticated) {
            this.props.history.push('/');
        }

        if (nextProps.authentication.loginFailed === true) {
            this.setState({
                loginRequested: false
            })
        }
    }

    render() {

        const {classes} = this.props;
        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline/>
                <div className={classes.paper}>
                    <Avatar className={classes.avatar}>
                        <FontAwesomeIcon icon={faUser}/>
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <form className={classes.form} noValidate onSubmit={this.handleSubmit}>
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            value={this.state.email}
                            onChange={this.handleChange}
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
                            autoComplete="current-password"
                            value={this.state.password}
                            onChange={this.handleChange}
                        />
                        { this.props.authentication.loginFailed && (
                            <Typography
                                className={classes.loginFailed}
                                component="h6"
                            >
                                Login failed! Please check your credentials.
                            </Typography>
                        )
                        }
                        <div className={classes.buttonContainer}>
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                color="primary"
                                className={classes.submit}
                                disabled={!this.validateForm() || this.state.loginRequested}
                            >
                                Sign In
                            </Button>
                            {
                                this.state.loginRequested && (
                                    <CircularProgress className={classes.progress}/>
                                )
                            }
                        </div>
                        <Grid container>
                            <Grid item xs>
                                <Link href="#" variant="body2">
                                    Forgot password?
                                </Link>
                            </Grid>
                        </Grid>
                    </form>
                </div>
            </Container>
        );
    }
}

function mapDispatchToProps(dispatch) {
    return {
        authenticate: (email, password) => {dispatch(authenticate(email,password))}
    }
}

const mapStateToProps = state => {
    return {
        authentication: state.authentication
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(withStyles(styles)(Login)));

