import Vue from 'vue';
import Router from 'vue-router';
import VueSessionStorage from 'vue-sessionstorage';
import Login from '../components/Login.vue';
import ManageHome from '../components/Manage/ManageHome.vue';
import StudentAssign from '../components/Student/StudentAssign.vue';
import StudentGrades from '../components/Student/StudentGrades.vue';

Vue.use(Router);
Vue.use(VueSessionStorage);

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
      path: '/grades',
      name: 'StudentGrades',
      component: StudentGrades,
    },
    {
      path: '/',
      name: 'StudentAssign',
      component: StudentAssign,
    },
  ],
});
