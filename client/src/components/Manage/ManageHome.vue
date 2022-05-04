<template>
  <div class="container-lg border-top border-bottom rounded py-2">
    <button
        type="button"
        class="btn btn-success btn-md float-right">
      <div v-if="this.$session.get('user') != undefined">
        {{ this.$session.get('user') }}
      </div>
      <div v-else>
        Login
      </div>
    </button>
    <a href='http://localhost:8080/'>
      <button
          type="button"
          class="btn btn-secondary btn-md float-right mx-2">
          <div>
            Student
          </div>
      </button>
    </a>
    <div class="row">
      <h1>Manage Course</h1>
    </div>
    <br>
    <div class="row">
      <div v-show="showComp==='manage_home'"
      class="btn-group-vertical col-sm-3 left-button-group" height="250px">
        <button class="btn btn-primary" type="button"
        @click="showComp = 'manage_class'">Edit Students</button>
        <br>
        <button class="btn btn-primary" type="button"
        @click="showComp = 'manage_ta'">Edit TAs</button>
        <br>
        <button class="btn btn-primary" type="button"
        @click="showComp = 'manage_assign'">Edit Assignments</button>
        <br>
        <button class="btn btn-primary" type="button"
        @click="downloadGradesCSV()">Download Grades</button>
      </div>
      <div class="col-12 </div>">
        <div v-show="this.showComp==='manage_class'">
          <ManageClass />
        </div>
        <div v-show="this.showComp==='manage_assign'">
          <ManageAssign />
        </div>
        <div v-show="this.showComp==='manage_ta'">
          <ManageTA />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  .list-group{
      height: 250px;
      margin-bottom: 10px;
      overflow:scroll;
      -webkit-overflow-scrolling: touch;
      outline:solid;
  }
  .left-button-group{
    height: 250px;
  }
</style>

<script>
import Vue from 'vue';
import VueSessionStorage from 'vue-sessionstorage';
import axios from 'axios';

import ManageTA from './ManageTA.vue';
import ManageAssign from './ManageAssign/ManageAssign.vue';
import ManageClass from './ManageClass.vue';

Vue.use(VueSessionStorage);
Vue.config.productionTip = false;

export default {
  data() {
    return {
      showComp: '',
      gradeHeaders: '',
      gradeData: [],
    };
  },
  components: {
    ManageTA,
    ManageAssign,
    ManageClass,
  },
  computed: {
    manageComponent() {
      if (this.showComp === 'manage_assign') {
        return 'ManageAssignDefault';
      } if (this.showComp === 'manage_class') {
        return 'ManageClass';
      } if (this.showComp === 'manage_ta') {
        return 'ManageTA';
      } if (this.showComp === 'manage_home') {
        return 'ManageHome';
      }
      return '';
    },
  },
  methods: {
    getGradesData() {
      const path = 'http://localhost:5000/gradesdata';
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.gradeHeaders = res.data.headers;
          this.gradeData = res.data.grades;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    downloadGradesCSV() {
      // Make API call
      this.getGradesData();
      let csv = this.gradeHeaders;
      const csvdata = this.gradeData;
      csvdata.forEach((row) => {
        csv += row.join(',');
        csv += '\n';
      });
      const anchor = document.createElement('a');
      anchor.href = `data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`;
      anchor.target = '_blank';
      anchor.download = 'student_grades.csv';
      anchor.click();
    },
  },
  created() {
    if (this.$session.get('is_TA') === 'false') {
      this.$router.push('/login?unauthorized=true');
    }
    this.showComp = 'manage_home';
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.getGradesData();
  },
};
</script>
