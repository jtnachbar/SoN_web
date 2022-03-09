<template>
    <ul class="list-group">
        <li class="list-group-item">Cras justo odio</li>
        <li class="list-group-item">Dapibus ac facilisis in</li>
        <li class="list-group-item">Morbi leo risus</li>
        <li class="list-group-item">Porta ac consectetur ac</li>
        <li class="list-group-item">Vestibulum at eros</li>
    </ul>
</template>

<script>
import Vue from 'vue';
import axios from 'axios';
import VueSessionStorage from 'vue-sessionstorage';

Vue.use(VueSessionStorage);
Vue.config.productionTip = false;

export default {
  data() {
    return {
      TAs: [],
    };
  },
  components: {
  },
  methods: {
    getTAs() {
      const path = 'http://localhost:5000/manage/student';
      axios.get(path, {
        params: {
          get_ta: 'true',
        },
      })
        .then((res) => {
          this.TAs = res.data.students;
          console.log(this.TAs);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getTAs();
  },
};
</script>
