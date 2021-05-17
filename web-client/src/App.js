import React, {Fragment, useState, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css'
import './App.css';

import Login from "./components/Login";

import useToken from "./components/useToken";
import DashBoard from "./components/DashBoard";
import Menu from "./components/Menu";


function App() {

    const {user: currentUser} = useSelector((state) => state.auth);

    const dispatch = useDispatch();
    console.log(currentUser);

    return (
        <BrowserRouter>
            <Fragment>
                <Menu />
                <Switch>
                    <Route exact path="/login" component={Login} />
                    <Route path="/dashboard">
                        <DashBoard/>
                    </Route>
                </Switch>
            </Fragment>
        </BrowserRouter>
    );
}

export default App;
