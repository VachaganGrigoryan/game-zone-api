import React, {Component} from 'react';


async function loginUserWithRefresh(token) {
    return fetch('http://127.0.0.1:8000/api/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(token)
    }).then(data => data.json())
}


class DashBoard extends Component {
    constructor(props) {
        super(props);
        console.log(props)
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        };
    }

    componentDidMount() {
        fetch("http://127.0.0.1:8000/api/dashboard/", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.props.token.access}`
            }
        }).then(response => {
            if (response.status === 401) {

                fetch('http://127.0.0.1:8000/api/token/refresh/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "refresh": this.props.token.refresh
                    })
                }).then(data => {
                    console.log(data.json());
                    this.props.setToken(data.json())
                })

            }
        }).then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result
                    });
                },
                // Note: it's important to handle errors here
                // instead of a catch() block so that we don't swallow
                // exceptions from actual bugs in components.
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    render() {
        const {error, isLoaded, items} = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <ul>{items.username}</ul>
            );
        }
    }
}

export default DashBoard;