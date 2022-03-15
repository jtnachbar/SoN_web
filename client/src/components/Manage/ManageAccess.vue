<template>
    <div class="container">
      <div class="col-md-10">
        <h1> The website is {{ web_status }} </h1>
        <h2> Bring not {{ web_status }} </h2>
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
