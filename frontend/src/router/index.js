import Vue from 'vue'
import VueRouter from 'vue-router'
import FeedView from "@/views/FeedView.vue";
import AuthorizeView from "@/views/AuthorizeView.vue";

import store from "../store"

Vue.use(VueRouter)

const routes = [
  {
    path: '/auth',
    name: 'auth',
    component: AuthorizeView
  },
  {
    path: '/',
    name: 'feed',
    component: FeedView,
    meta: {
      requiresAuth: true
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router


router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {

    // if (window.$cookies.get('token') === null) {
    if (localStorage.getItem("token") === null) {
      next('/auth')
    } else {
      next()
    }
  } else {
    if ((to.path === '/auth' || to.path === '/register') && store.getters.getLoggedIn === true) {
      next('/')
    } else {
      next()
    }
  }
})
