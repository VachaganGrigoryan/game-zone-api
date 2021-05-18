import axios from "axios";

const API_URL = "http://localhost:8000/api";

const register = (first_name, last_name, username, password) => {
    return axios.post(`${API_URL}/account/register/`, {
        first_name,
        last_name,
        username,
        password,
    });
};

const login = (username, password) => {
    return axios.post(`${API_URL}/token/`, {
        username,
        password,
    })
        .then((response) => {
            if (response.data.access) {
                localStorage.setItem("user", JSON.stringify(response.data));
            }

            return response.data;
        });
};

const refresh = (refreshToken) => {
    return axios.post(`${API_URL}/token/refresh/`, {
        "refresh": refreshToken
    })
        .then((response) => {
            if (response.data.access) {
                localStorage.setItem("user", JSON.stringify(response.data));
            }

            return response.data;
        });
};

const logout = () => {
    localStorage.removeItem("user");
};

// eslint-disable-next-line import/no-anonymous-default-export
export default {
    register,
    login,
    refresh,
    logout,
};
