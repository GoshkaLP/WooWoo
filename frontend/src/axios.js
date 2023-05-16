import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "http://localhost:8000",
});

axiosInstance.interceptors.request.use(function (config) {
    let token = localStorage.getItem("token");
    config.headers["Authorization"] = "Bearer " + token;
    return config;
});

export default axiosInstance;
