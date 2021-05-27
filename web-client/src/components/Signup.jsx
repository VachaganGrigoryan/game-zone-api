import React, {useRef, useState} from "react";
import {useDispatch, useSelector} from "react-redux";

import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";
import {isEmail} from "validator";

import {signup} from "../actions/auth";

const required = (value) => {
    if (!value) {
        return (
            <div className="alert alert-danger" role="alert">
                This field is required!
            </div>
        );
    }
};

const validEmail = (value) => {
    if (!isEmail(value)) {
        return (
            <div className="alert alert-danger" role="alert">
                This is not valid email.
            </div>
        )
    }
}


const vusername = (value) => {
  if (value.length < 3 || value.length > 20) {
    return (
      <div className="alert alert-danger" role="alert">
        The username must be between 3 and 20 characters.
      </div>
    );
  }
};

const vpassword = (value) => {
  if (value.length < 6 || value.length > 40) {
    return (
      <div className="alert alert-danger" role="alert">
        The password must be between 6 and 40 characters.
      </div>
    );
  }
};


function Signup(props) {
    const form = useRef();
    const checkBtn = useRef();

    const [username, setUsername] = useState();
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [password, setPassword] = useState();
    const [success, setSuccess] = useState(false);

    // const {message} = useSelector(state => state.message);

    const dispatch = useDispatch();

    const onChangeUsername = (e) => {
        const username = e.target.value;
        setUsername(username);
    };

    const onChangeFirstName = (e) => {
        const firstName = e.target.value;
        setFirstName(firstName);
    };

    const onChangeLastName = (e) => {
        const lastName = e.target.value;
        setLastName(lastName);
    };

    const onChangePassword = (e) => {
        const password = e.target.value;
        setPassword(password);
    };

    const handleSignup = (e) => {
        e.preventDefault();

        setSuccess(false);

        form.current.validateAll();

        if (checkBtn.current.context._errors.length === 0) {
            dispatch(signup(username, firstName, lastName, password))
                .then(() => {
                    setSuccess(true);
                })
                .catch(() => {
                    setSuccess(false);
                });
        }
    };

    return (
        <main className="form-signup">
            <Form onSubmit={handleSignup} ref={form}>

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
                    {/*<button className="w-100 btn btn-lg btn-primary" disabled={loading}>*/}
                    {/*    {loading && (*/}
                    {/*        <span className="spinner-border spinner-border-sm"></span>*/}
                    {/*    )}*/}
                    {/*    <span>Login</span>*/}
                    {/*</button>*/}
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

export default Signup;