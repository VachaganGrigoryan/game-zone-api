import React, {Fragment, useState, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css'
import './App.css';

import Login from "./components/Login";

import DashBoard from "./components/DashBoard";
import Menu from "./components/Menu";


function App() {

    const {user: currentUser} = useSelector((state) => state.auth);

    const dispatch = useDispatch();
    console.log(currentUser);

    return (
        <BrowserRouter>
            <Fragment>
                <Menu currentUser={currentUser} />
                <Switch>
                    <Route exact path="/login" component={Login} />
                    <Route exact path="/dashboard" component={DashBoard}/>
                </Switch>
            </Fragment>
        </BrowserRouter>
    );
}

export default App;
