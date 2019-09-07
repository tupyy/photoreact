import React from 'react';
import { Translate, translate } from 'react-jhipster';
import { Link } from 'react-router-dom';

export interface ILoginModalProps {
    loginError: boolean;
    handleLogin: Function;
}

interface ILoginFormState {
    username: string;
    password: string;
}

class LoginForm extends React.Component<ILoginModalProps, ILoginFormState> {
    constructor(props) {
        super(props);

        this.state = {
            'username': 'cosmin',
            'password': 'cosmin'
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(event) {
        const {handleLogin} = this.props;
        handleLogin(this.state.username, this.state.password, false)
    }
    handleChange(event) {
        if (event.target.name === "username") {
            this.setState({"username": event.target.value})
        } else {
            this.setState({"password": event.target.event})
        }
    }

    render() {
        const { loginError } = this.props;

        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Username
                    <input type="text" placeholder="Enter username" name="username" value={this.state.username} onChange={this.handleChange}/>
                    </label>
                    <label>
                        Password
                    <input type="password" name="password" value={this.state.password} onChange={this.handleChange} />
                    </label>
                    <button type="submit">Login</button>
                </form>
            </div>
        );
    }
}

export default LoginForm;
