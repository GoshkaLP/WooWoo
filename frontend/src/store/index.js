import Vue from 'vue'
import Vuex from 'vuex'
import usersModule from "@/store/modules/usersModule";
import feedModule from "@/store/modules/feedModule";

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    usersModule,
    feedModule
  }
})
