<template>
  <div class="container">
    <div class="row vertical-center-row">
      <div class="col text-center">
        <h1 v-if="this.$route.query.unauthorized==='true'"> Unauthorized, please log in </h1>
        <h1 v-else> Please log in </h1>
        <br>
        <a href='https://secure.its.yale.edu/cas/?service=http%3A%2F%2Flocalhost%3A8080/login'>
          <button class="btn btn-large btn-primary">
          Login: {{ this.$session.get('user') }} </button>
        </a>
        <br><br>
        <h2 v-if="showProblem===true"> There was a problem, please try again </h2>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import VueSessionStorage from 'vue-sessionstorage';
import axios from 'axios';

Vue.use(VueSessionStorage);
Vue.config.productionTip = false;

export default {
  name: 'Login',
  data() {
    return {
      ticket: '',
      showProblem: false,
    };
  },
  created() {
    if (typeof this.$route.query.ticket !== 'undefined') {
      const path = `http://localhost:5000/login/${this.$route.query.ticket}`;
      axios.get(path, { responseType: 'text' })
        .then((res) => {
          this.$session.set('user', res.data.username);
          this.$session.set('is_TA', res.data.is_TA);
          this.$session.set('token', res.data.token);
          window.location.href = 'http://localhost:8080/';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
};
</script>
