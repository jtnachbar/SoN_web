<template>
  <div class="container-lg border-top border-bottom rounded py-2">
    <button
        type="button"
        class="btn btn-success btn-md float-right">
        <div>
          {{ this.$session.get('user') }}
        </div>
    </button>
    <a href='http://localhost:8080/manage'>
      <button v-if="this.$session.get('is_TA') === 'true'"
          type="button"
          class="btn btn-secondary btn-md float-right mx-2">
          <div>
            Manage
          </div>
      </button>
    </a>
    <a href='http://localhost:8080/'>
      <button
          type="button"
          class="btn btn-warning btn-md float-right">
          <div>
            Assignments
          </div>
      </button>
    </a>
    <div class="row">
      <h1>Grades</h1>
    </div>
    <div>
      <div v-for="assign in grades" v-bind:key="assign.name">
        <div class="row py-2 px-3 align-middle">
          <button class="col-2 btn-lg btn-primary mr-2 " @click="toggleExpandedAssign(assign.name)">
            {{ assign.name }} </button>
          <h4 class="col-2"> {{ assign.points }} / {{ assign.total_points }}</h4>
        </div>
        <div v-if="expandedAssign===assign.name">
          <div v-for="question in assign.questions" v-bind:key="question.name">
            <div class="row py-2 pl-4 align-middle">
              <button class="col-2 btn btn-secondary mr-2 "
              @click="toggleExpandedQuestion(question.name)">
              {{ question.name }} </button>
              <h5 class="col-2"> {{ question.points }} / {{ question.total_points }}</h5>
            </div>
            <div v-if="expandedQuestion===question.name">
              <div v-for="part in question.parts" v-bind:key="part.part_num">
                <div class="row py-2 pl-5 align-middle">
                <button class="col-1 btn btn-secondary mr-2">
                {{ part.part_num}} </button>
                <h5 class="col-2"> {{ part.points }} / {{ part.total }}</h5>
              </div>
              </div>
            </div>
          </div>
        </div>
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
  data() {
    return {
      expandedAssign: '',
      expandedQuestion: '',
      grades: {},
    };
  },
  methods: {
    getGrades() {
      const path = 'http://localhost:5000/student/grades';
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.grades = res.data.grades;
          console.log(this.grades);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    toggleExpandedAssign(name) {
      if (name === this.expandedAssign) {
        this.expandedAssign = '';
      } else {
        this.expandedAssign = name;
      }
    },
    toggleExpandedQuestion(name) {
      if (name === this.expandedQuestion) {
        this.expandedQuestion = '';
      } else {
        this.expandedQuestion = name;
      }
    },
  },
  created() {
    console.log(this.$session.get('user'));
    if (this.$session.get('user') === undefined) {
      this.$router.push('/login?unauthorized=true');
    }
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.getGrades();
  },
};
</script>
