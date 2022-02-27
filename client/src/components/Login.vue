<template>
  <a href='https://secure.its.yale.edu/cas/?service=http%3A%2F%2Flocalhost%3A8080/login'>
    <button> Login: {{ this.$session.get('user') }} </button>
  </a>
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
    };
  },
  methods: {
    verifyLogin() {
    },
  },
  created() {
    if (typeof this.$route.query.ticket !== 'undefined') {
      const path = `http://localhost:5000/login/${this.$route.query.ticket}`;

      axios.get(path, { responseType: 'text' })
        .then((res) => {
          console.log(res.data.username);
          this.$session.set('user', res.data.username);
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
