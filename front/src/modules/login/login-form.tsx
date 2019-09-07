import React, {useState} from 'react';

export interface ILoginModalProps {
    loginError: boolean;
    handleLogin: Function;
}

const LoginForm = (props: ILoginModalProps) => {
    const [username, setUsername] = useState('cosmin');
    const [password, setPassword] = useState('cosmin');

    const handleSubmit = (event) => {
            event.preventDefault();
            const {handleLogin} = props;
            handleLogin(username,password, false)
        };

    const handleChange = (event: any) => {
        const method = event.target.name === "username" ? setUsername : setPassword;
        method(event.targe.value);
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>
                    Username
                    <input type="text" placeholder="Enter username" name="username" value={username}
                           onChange={handleChange}/>
                </label>
                <label>
                    Password
                    <input type="password" name="password" value={password}
                           onChange={handleChange}/>
                </label>
                <button type="submit">Login</button>
            </form>
        </div>
    )
};

export default LoginForm;

