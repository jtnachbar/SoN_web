import Vue from 'vue';
import Router from 'vue-router';
import Login from '../components/Login.vue';
import ManageHome from '../components/Manage/ManageHome.vue';
import StudentAssign from '../components/Student/StudentAssign.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/manage',
      name: 'ManageHome',
      component: ManageHome,
    },
    {
      path: '/',
      name: 'StudentAssign',
      component: StudentAssign,
    },
  ],
});
