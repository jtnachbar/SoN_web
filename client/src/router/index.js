import Vue from 'vue';
import Router from 'vue-router';
import Books from '../components/Books.vue';
import Login from '../components/Login.vue';
import Manage from '../components/Manage.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Books',
      component: Books,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/manage',
      name: 'Manage',
      component: Manage,
    },
  ],
});
