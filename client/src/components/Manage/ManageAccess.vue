<template>
  <div>
    <div class="container">
      <div class='row'>
        <h1> The website is {{ web_status }} </h1>
      </div>
      <div class='row'>
        <button @click="$parent.showComp = 'manage_home';"
          class="btn btn-secondary mr-2">
          &laquo; Back
        </button>
        <button v-if = "web_status === 'offline'" class = "btn btn-success"
        @click="updateStatus( {status: 'online'})"> Bring site up </button>
        <button v-if = "web_status === 'online'" class = "btn btn-danger"
        @click="updateStatus( {status: 'offline'})"> Take site down </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      web_status: '',
      token: '',
      user: '',
    };
  },
  methods: {
    checkStatus() {
      const path = 'http://localhost:5000/status';
      axios.get(path)
        .then((res) => {
          this.web_status = res.data.status;
          console.log(this.web_status);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateStatus(payload) {
      const path = 'http://localhost:5000/status';
      axios.put(path, payload, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.checkStatus();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.checkStatus();
        });
    },
  },
  created() {
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.checkStatus();
  },
};
</script>
