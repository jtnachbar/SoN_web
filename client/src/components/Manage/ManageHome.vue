<template>
  <div class="container-lg border-top border-bottom rounded py-5">
    <button
        type="button"
        class="btn btn-success btn-md float-right"
        @click="login()">
      {{ this.$session.get('user') }}
    </button>
    <div class="row">
      <h1>Manage Course</h1>
    </div>
    <br>
    <div class="row">
      <div class="btn-group-vertical col-sm-3" height="250px">
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
        @click="showComp = 'manage_access'">Disable Access</button>
      </div>
      <div class="col-md-8 </div>">
        <component :is="manageComponent"></component>
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
</style>

<script>
import Vue from 'vue';
import VueSessionStorage from 'vue-sessionstorage';
import ManageTA from './ManageTA.vue';
import ManageAssign from './ManageAssign.vue';
import ManageClass from './ManageClass.vue';
import ManageAccess from './ManageAccess.vue';

Vue.use(VueSessionStorage);
Vue.config.productionTip = false;

export default {
  data() {
    return {
      showComp: '',
    };
  },
  components: {
    ManageTA,
    ManageAssign,
    ManageClass,
    ManageAccess,
  },
  computed: {
    manageComponent() {
      if (this.showComp === 'manage_assign') {
        return 'ManageAssign';
      } if (this.showComp === 'manage_class') {
        return 'ManageClass';
      } if (this.showComp === 'manage_ta') {
        return 'ManageTA';
      } if (this.showComp === 'manage_access') {
        return 'ManageAccess';
      }
      return '';
    },
  },
  methods: {

  },
  created() {
    this.showComp = '';
  },
};
</script>
