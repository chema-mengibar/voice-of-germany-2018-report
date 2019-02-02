import Vue from 'vue'
import Router from 'vue-router'
// import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      alias: '/home',
      name: '',
      component: () => import( /* webpackChunkName: "home" */ './views/Home.vue' )
    },
    {
      path: '/about_project',
      name: 'about_project',
      component: () => import( /* webpackChunkName: "about_project" */ './views/AboutProject.vue' )
    }
  ]
})
