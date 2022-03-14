import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Home from '../views/Home.vue'

import Alertas from '../views/Alertas.vue'
import Alerta from '../views/Alerta.vue'
//import Category from '../views/Category.vue'
//import Search from '../views/Search.vue'
//import Cart from '../views/Cart.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import RedZones from '../views/RedZones.vue'
import Camera from '../views/Camera.vue'
import Audio from '../views/Audio.vue'
//import MyAccount from '../views/MyAccount.vue'
//import Checkout from '../views/Checkout.vue'
//import Success from '../views/Success.vue'
import Cameras from '../views/Cameras.vue'
import Resumo from '../views/Resumo.vue'
import SandBox from '../views/SandBox.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LogIn
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',

    component: LogIn
  },
    {
    path: '/red_zones',
    name: 'RedZones',
    component: RedZones
  },
  {
    path: '/audio',
    name: 'Audio',
    component: Audio
  },
  {
    path: '/:category_slug/:alert_slug',
    name: 'Alerta',
    component: Alerta
  },
  {
    path: '/red_zone/:slug_cam',
    name: 'Camera',
    component: Camera
  },
    {
    path: '/latest-alerts/:page',
    name: 'latest_alerts',
    component: Alertas
  },
  {
    path: '/:category_slug',
    name: 'Category',
    component: Category
  },
  {
    path: '/cameras',
    name: 'Cameras',
    component: Cameras
  },
  {
    path: '/resumo',
    name: 'Resumo',
    component: Resumo
  },
  {
    path: '/SandBox',
    name: 'SandBox',
    component: SandBox
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (!store.state.isAuthenticated && to.path != "/log-in") { //record => record.meta.requireLogin) &&
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router