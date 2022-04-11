<template>
  <div>
    <div class="container">
      <div class="col-md-10">
        <h1> The website is {{ web_status }} </h1>
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
      axios.put(path, payload)
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
    this.checkStatus();
  },
};
</script>
