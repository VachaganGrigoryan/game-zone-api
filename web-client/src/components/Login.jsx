import React, {useRef, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {Redirect} from 'react-router-dom';

import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";

import {login} from "../actions/auth";

import '../css/Լogin.css';

const required = (value) => {
    if (!value) {
        return (
            <div className="alert alert-danger" role="alert">
                This field is required!
            </div>
        );
    }
};


function Login(props) {
    const form = useRef();
    const checkBtn = useRef();

    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [loading, setLoading] = useState(false);

    const {isLoggedIn} = useSelector(state => state.auth);
    // const {message} = useSelector(state => state.message);

    const dispatch = useDispatch();

    const onChangeUsername = (e) => {
        const username = e.target.value;
        setUsername(username);
    };

    const onChangePassword = (e) => {
        const password = e.target.value;
        setPassword(password);
    };

    const handleLogin = (e) => {
        e.preventDefault();

        setLoading(true);

        form.current.validateAll();

        console.log(username, password)
        if (checkBtn.current.context._errors.length === 0) {
            dispatch(login(username, password))
                .then(() => {
                    props.history.push("/profile");
                    window.location.reload();
                })
                .catch(() => {
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    };
    console.log(isLoggedIn);

    if (isLoggedIn) {
        return <Redirect to="/profile"/>;
    }

    return (
        <main className="form-signin">
            <Form onSubmit={handleLogin} ref={form}>

                <h1 className="h3 mb-3 fw-normal">Please sign in</h1>
                {/*//     <div className="form-floating">*/}
                {/*//         <input type="text" className="form-control" id="floatingInput"*/}
                {/*//                placeholder="Username" onChange={e => setUserName(e.target.value)}/>*/}
                {/*//         <label htmlFor="floatingInput">Username</label>*/}
                {/*//     </div>*/}
                {/*//     <div className="form-floating">*/}
                {/*//         <input type="password" className="form-control" id="floatingPassword"*/}
                {/*//                placeholder="Password" onChange={e => setPassword(e.target.value)}/>*/}
                {/*        <label htmlFor="floatingPassword">Password</label>*/}
                {/*    </div>*/}
                <div className="form-floating">
                    <Input
                        type="text"
                        className="form-control"
                        name="username"
                        placeholder="Username"
                        value={username}
                        onChange={onChangeUsername}
                        validations={[required]}
                    />
                    {/*<label htmlFor="username">Username</label>*/}
                </div>

                <div className="form-floating">
                    <Input
                        type="password"
                        className="form-control"
                        placeholder="Password"
                        name="password"
                        value={password}
                        onChange={onChangePassword}
                        validations={[required]}
                    />
                    {/*<label htmlFor="password">Password</label>*/}
                </div>

                <div className="form-group">
                    <button className="w-100 btn btn-lg btn-primary" disabled={loading}>
                        {loading && (
                            <span className="spinner-border spinner-border-sm"></span>
                        )}
                        <span>Login</span>
                    </button>
                </div>

                {/*{message && (*/}
                {/*    <div className="form-group">*/}
                {/*        <div className="alert alert-danger" role="alert">*/}
                {/*            {message}*/}
                {/*        </div>*/}
                {/*    </div>*/}
                {/*)}*/}
                <CheckButton style={{display: "none"}} ref={checkBtn}/>
            </Form>
            {/*// <form onSubmit={handleSubmit}>*/}
            {/*//     <h1 className="h3 mb-3 fw-normal">Please sign in</h1>*/}
            {/*//*/}
            {/*//     <div className="form-floating">*/}
            {/*//         <input type="text" className="form-control" id="floatingInput"*/}
            {/*//                placeholder="Username" onChange={e => setUserName(e.target.value)}/>*/}
            {/*//         <label htmlFor="floatingInput">Username</label>*/}
            {/*//     </div>*/}
            {/*//     <div className="form-floating">*/}
            {/*//         <input type="password" className="form-control" id="floatingPassword"*/}
            {/*//                placeholder="Password" onChange={e => setPassword(e.target.value)}/>*/}
            {/*        <label htmlFor="floatingPassword">Password</label>*/}
            {/*    </div>*/}

            {/*    <button className="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>*/}
            {/*    <p className="mt-5 mb-3 text-muted">© 2021 </p>*/}
            {/*</form>*/}
        </main>
    )
}

export default Login;