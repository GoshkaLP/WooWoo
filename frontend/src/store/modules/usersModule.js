import axiosInstance from "@/axios";


const state = {
    loggedIn: false,
    authForm: {
        state: null,
        message: ''
    },
    registerForm: {
        state: null,
        message: ''
    },
    changePassForm: {
        state: null,
        message: ''
    }
};

const actions = {
    async authUser(state, user) {
        try {
            const response = await axiosInstance.post("/api/users/login", user);
            if ("access_token" in response.data) {
                localStorage.setItem("token", response.data.access_token);
                state.commit("setLoggedIn", true);
            }
        } catch (error) {
            let error_detail = error.response.data.detail
            if (error_detail === "User not found") {
                state.commit("setAuthForm", {
                    state: false,
                    message: "Данного пользователя не существует"
                })
            } else if (error_detail === "Wrong password") {
                state.commit("setAuthForm", {
                    state: false,
                    message: "Неверный пароль"
                })
            }
        }
    },

    // async registerUser(state, user) {
    //     const response = await axiosInstance.post("/api/users/register/email", user);
    //     console.log(response);
    //     if (response.data.message === 'ACCOUNT_ALREADY_EXISTS') {
    //         state.commit("setRegisterForm", {
    //             state: false,
    //             message: "Данный пользователь уже существует"
    //         });
    //         console.log("not regged")
    //     } else if (response.data.message === "SUCCESS") {
    //         localStorage.setItem("token", response.data.data.token);
    //         console.log("regged");
    //         state.commit("setLoggedIn", true);
    //     }
    // },
    //
    // async logoutUser(state) {
    //     const response = await axiosInstance.get("/api/users/logout");
    //     console.log(response)
    //     if (response.data.message === "SUCCESS") {
    //         state.commit("setLoggedIn", false);
    //         state.commit("clearUnits");
    //         // window.$cookies.remove("token");
    //         localStorage.removeItem("token");
    //     }
    // },
    //
    // async changePassword(state, passwordData) {
    //     // for (var pair of passwordData.entries()) {
    //     //     console.log(pair[0]+ ', ' + pair[1]);
    //     // }
    //
    //     const response = await axiosInstance.post('/api/users/change/password/email', passwordData);
    //     if (response.data.message === "SUCCESS") {
    //         state.commit("setChangePassForm", {
    //             state: null,
    //             message: "SUCCESS"
    //         });
    //         localStorage.setItem("token", response.data.data.token);
    //
    //     } else if (response.data.message === "WRONG_PASSWORD") {
    //         state.commit("setChangePassForm", {
    //             state: false,
    //             message: "Вы ввели неверный текущий пароль"
    //         })
    //     } else if (response.data.message === "OLD_PASSWORD") {
    //         state.commit("setChangePassForm", {
    //             state: false,
    //             message: "Ваш новый пароль совпадает со старым"
    //         })
    //     }
    // }
};

const mutations = {
    // sync
    setLoggedIn(state, payload) {
        state.loggedIn = payload;
    },

    setAuthForm(state, payload) {
        state.authForm.state = payload.state;
        state.authForm.message = payload.message;
    },
    setRegisterForm(state, payload) {
        state.registerForm.state = payload.state;
        state.registerForm.message = payload.message;
    },
    setChangePassForm(state, payload) {
        state.changePassForm.state = payload.state;
        state.changePassForm.message = payload.message;
    }
};


const getters = {
    getLoggedIn(state) {
        return state.loggedIn;
    },

    getAuthForm(state) {
        return state.authForm;
    },
    getRegisterForm(state) {
        return state.registerForm;
    },
    getChangePassForm(state) {
        return state.changePassForm;
    }
};


export default {
    state,
    actions,
    mutations,
    getters
}