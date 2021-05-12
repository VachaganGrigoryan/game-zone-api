import React from "react";
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import './App.css';
import Login from "./components/Login";
import useToken from "./components/useToken";
import DashBoard from "./components/DashBoard";

function App() {

    const {token, setToken} = useToken();
    console.log(token);
    if (!token) {
        return <Login setToken={setToken}/>
    }

    return (
        <div className="wrapper">
            <h1>Application</h1>
            <BrowserRouter>
                <Switch>
                    <Route path="/dashboard">
                        <DashBoard token={token}/>
                    </Route>
                </Switch>
            </BrowserRouter>
        </div>
    );
}

export default App;
