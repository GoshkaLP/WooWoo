import axiosInstance from "@/axios";
import { Buffer } from 'buffer';

const state = {
    userFeed: {
        data: [],
        loaded: false
    },
    currentUser: {
        photo: null,
        interests: [],
        loaded: false
    },
    userLike: {
        like: null,
        match: null,
        loaded: false
    }
};

const actions = {
    async fetchFeed(state) {
        state.commit("setUserFeedLoaded", false);
        state.commit("clearUserFeedData");
        try {
            const response = await axiosInstance.get("/api/feed/user/feed");
            if (response.data.length !== 0) {
                response.data.forEach(userForm => {
                    state.commit("addUserFeedData", userForm);
                });
            }
            state.commit("setUserFeedLoaded", true);
        } catch (error) {
            console.log(error);
        }
    },
    async fetchCurrentUser(state, user_id) {
        state.commit("setCurrentUserLoaded", false);
        state.commit("clearUserFeedPhoto");
        state.commit("clearUserFeedInterests");
        // будем использовать одно фото
        try {
            const photo_urls_response = await axiosInstance.get("/api/forms/user/"+user_id+"/photo");
            const photo_response = await axiosInstance.get(photo_urls_response.data[0].photo_url, {
                responseType: "arraybuffer"
            });
            let photo = Buffer.from(photo_response.data, 'binary').toString('base64');
            state.commit("addUserPhoto", photo);

            const interests_response = await axiosInstance.get("/api/forms/user/"+user_id+"/interests");
            interests_response.data.forEach(interest => {
                state.commit("addUserInterest", interest);

            });
            state.commit("setCurrentUserLoaded", true);
        } catch (error) {
            console.log(error);
        }
    },
    async setLike(state, user) {
        state.commit("setUserLikeLoaded", false);
        state.commit("clearUserLike");
        state.commit("clearUserMatch");
        try {
            const response = await axiosInstance.post("/api/feed/user/like", user);
            state.commit("addUserLike", response.data.like);
            state.commit("addUserMatch", response.data.match);
            state.commit("setUserLikeLoaded", true);
        } catch (error) {
            console.log(error);
        }
    }
};

const mutations = {
    addUserFeedData(state, payload) {
        state.userFeed.data.push(payload);
    },
    addUserPhoto(state, payload) {
        state.currentUser.photo = payload;
    },
    addUserInterest(state, payload) {
        state.currentUser.interests.push(payload);
    },
    setUserFeedLoaded(state, payload) {
        state.userFeed.loaded = payload;
    },
    clearUserFeedData(state) {
        state.userFeed.data = [];
    },
    clearUserFeedPhoto(state) {
        state.currentUser.photo = null;
    },
    clearUserFeedInterests(state) {
      state.currentUser.interests = [];
    },
    setUserLikeLoaded(state, payload) {
      state.userLike.loaded = payload;
    },
    setCurrentUserLoaded(state, payload) {
      state.currentUser.loaded = payload;
    },
    addUserLike(state, payload) {
        state.userLike.like = payload;
    },
    addUserMatch(state, payload) {
        state.userLike.match = payload;
    },
    clearUserLike(state) {
        state.userLike.like = null;
    },
    clearUserMatch(state) {
        state.userLike.match = null;
    }
};

const getters = {
    getUserFeed(state) {
        return state.userFeed;
    },
    getCurrentUser(state) {
        return state.currentUser;
    },
    getUserLike(state) {
        return state.userLike;
    }
};

export default {
    state,
    actions,
    mutations,
    getters
}
