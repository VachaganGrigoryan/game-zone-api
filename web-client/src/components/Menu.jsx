import React, {Fragment} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faChalkboard, faHome, faTachometerAlt, faUserCircle} from '@fortawesome/free-solid-svg-icons'
import {Link} from "react-router-dom";
import {useDispatch} from "react-redux";

import {logout} from "../actions/auth";


const Menu = ({currentUser}) => {
    console.log(currentUser);
    const dispatch = useDispatch();

    const handlerLogOut = () => {
        dispatch(logout());
    }

    return (
        <header>
            <div className="px-3 py-2 bg-dark text-white">
                <div className="container">
                    <div
                        className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
                        <a href="/"
                           className="d-flex align-items-center my-2 my-lg-0 me-lg-auto text-white text-decoration-none">
                            <FontAwesomeIcon icon={faChalkboard} className="bi d-block mx-auto mb-1"/>
                        </a>

                        <ul className="nav col-12 col-lg-auto my-2 justify-content-center my-md-0 text-small">
                            {currentUser && (
                                <Fragment>
                                    <li>
                                        <Link href="/" className="nav-link text-white">
                                            <FontAwesomeIcon icon={faHome} className="bi d-block mx-auto mb-1"/>
                                            Home
                                        </Link>
                                    </li>
                                    <li>
                                        <Link href="/dashboard" className="nav-link text-white">
                                            <FontAwesomeIcon icon={faTachometerAlt}
                                                             className="bi d-block mx-auto mb-1"/>
                                            Dashboard
                                        </Link>
                                    </li>
                                    <li>
                                        <Link to={"/profile"} className="nav-link text-white">
                                            <FontAwesomeIcon icon={faUserCircle} className="bi d-block mx-auto mb-1"/>
                                            {currentUser.username}
                                        </Link>
                                    </li>
                                </Fragment>
                            )}
                        </ul>
                    </div>
                </div>
            </div>
            <div className="px-3 py-2 border-bottom mb-3">
                <div className="container d-flex flex-wrap justify-content-center">
                    <form className="col-12 col-lg-auto mb-2 mb-lg-0 me-lg-auto">
                        <input type="search" className="form-control" placeholder="Search..." aria-label="Search"/>
                    </form>
                    {currentUser ? (
                        <div className="text-end">
                            <a href="/login" className="nav-link" onClick={handlerLogOut}>
                                LogOut
                            </a>
                        </div>
                    ) : (
                        <div className="text-end">
                            <Link to={"/login"} className="btn btn-outline-success me-2">
                                Login
                            </Link>
                            <Link to={"/register"} className="btn btn-outline-primary">
                                Sign Up
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Menu;