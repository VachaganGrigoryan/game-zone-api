import React, {Component} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faChalkboard, faHome, faTachometerAlt, faUserCircle} from '@fortawesome/free-solid-svg-icons'


function LoginButtons({token}) {

    if (!token) {
        return (
            <div className="text-end">
                <button type="button" className="btn btn-outline-success text-dark me-2">Login</button>
                <button type="button" className="btn btn-outline-primary">Sign-up</button>
            </div>
        )
    }

    return (
        <div className="text-end">
            <button type="button" className="btn btn-outline-warning text-dark me-2">Logout</button>
        </div>
    )

}


class Menu extends Component {
    constructor(props) {
        super(props);
    }

    render() {
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
                                <li>
                                    <a href="/" className="nav-link text-white">
                                        <FontAwesomeIcon icon={faHome} className="bi d-block mx-auto mb-1"/>
                                        Home
                                    </a>
                                </li>
                                <li>
                                    <a href="/dashboard" className="nav-link text-white">
                                        <FontAwesomeIcon icon={faTachometerAlt} className="bi d-block mx-auto mb-1"/>
                                        Dashboard
                                    </a>
                                </li>
                                <li>
                                    <a href="/profile" className="nav-link text-white">
                                        <FontAwesomeIcon icon={faUserCircle} className="bi d-block mx-auto mb-1"/>
                                        Customers
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div className="px-3 py-2 border-bottom mb-3">
                    <div className="container d-flex flex-wrap justify-content-center">
                        <form className="col-12 col-lg-auto mb-2 mb-lg-0 me-lg-auto">
                            <input type="search" className="form-control" placeholder="Search..." aria-label="Search"/>
                        </form>

                        <LoginButtons token={this.props.token}/>
                    </div>
                </div>
            </header>
        );
    }
}

export default Menu;