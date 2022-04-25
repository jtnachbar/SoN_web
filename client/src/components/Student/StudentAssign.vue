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
    <a href='http://localhost:8080/grades'>
      <button
          type="button"
          class="btn btn-warning btn-md float-right">
          <div>
            Grades
          </div>
      </button>
    </a>
    <div class="row">
      <h1>Assignments</h1>
    </div>
    <br>
    <div class="px-3 row">
        <h3 class='mr-2'> <b> Assignment: </b> {{ this.selected_assign.name}} </h3>
        <h3 class='mr-2' v-if="selected_question.name != ''" >
          <b> Question: </b> {{ this.selected_question.name}}
        </h3>
        <h3 v-if="selected_part.part_num != ''" >
          <b> Part: </b> {{ this.selected_part.part_num}}
        </h3>
    </div>
    <div class="px-3 row">
        <b-dropdown id="assign-drop" text="Select Assignment" class="mr-2 my-2">
        <b-dropdown-item v-for="assign in assignments" v-bind:key="assign.name"
        @click="getSelectedAssignment(assign.name); selected_assign.name = assign.name;
        selected_question = { name: '', format: '' }; getQuestions();">
          {{ assign.name }} </b-dropdown-item>
        </b-dropdown>

        <b-dropdown v-if="selected_assign.name != ''" id="question-drop" text="Select Question"
        class="mr-2 my-2">
        <b-dropdown-item v-for="question in questions" v-bind:key="question.name"
        @click="getSelectedQuestion(question.name); selected_question.name = question.name;
        selected_part = { part_num: '', direction: '' }; getAnswerStatus(); getParts();">
          {{ question.name }} </b-dropdown-item>
        </b-dropdown>

        <b-dropdown v-if="selected_question.name != ''" id="part-drop" text="Select Part"
        class="mr-4 my-2">
        <b-dropdown-item v-for="part in parts" v-bind:key="part.part_num"
        @click="getSelectedPart(part.part_num); getAnswer();">
          {{ part.part_num }} {{ grades[parseInt(part.part_num)] === true ?
          '&#9989;' : '&#10060;' }}
          </b-dropdown-item>
        </b-dropdown>
    </div>
    <hr>
    <div class="px-3 row">
      <a> {{ this.selected_question.format }} </a>
    </div>
    <hr>
    <div class="px-3 row">
      <a> {{ this.selected_part.direction }} </a>
    </div>
    <br>
    <div v-if="this.selected_part.direction !== ''" class="px-3 row">
      <input class="col-2 mr-2 form-control"
            placeholder="Answer" v-model="selected_answer.response"
            maxlength = "13">
      <button class='btn btn-success mb-2' @click="submitAnswer(); getAnswerDelay();">
        Submit </button>
      <h5 v-if="this.selected_answer.correct===null">
        <span class="ml-2 badge badge-secondary"> N/A </span> </h5>
      <h5 v-if="this.selected_answer.correct===true">
        <span class="ml-2 badge badge-success">  Correct </span> </h5>
      <h5 v-if="this.selected_answer.correct===false">
        <span class="ml-2 badge badge-danger"> Wrong </span> </h5>
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
      showComp: '',
      selected_assign: { name: '', active: '' },
      selected_question: { name: '', format: '' },
      selected_part: { part_num: '', direction: '' },
      selected_answer: { response: '', correct: '' },
      grades: {},
      assignments: [],
      questions: [],
      parts: [],
    };
  },
  components: {
  },
  methods: {
    getAnswerDelay() {
      setTimeout(() => this.getAnswer(), 500);
    },
    getAssignments() {
      const path = 'http://localhost:5000/student/assigns';
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.assignments = res.data.assignments;
          console.log(this.assignments);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSelectedAssignment(assignmentName) {
      const result = this.assignments.filter((a) => a.name === assignmentName);
      if (result !== []) {
        [this.selected_assign] = result;
      }
    },
    getQuestions() {
      const path = `http://localhost:5000/student/questions/${this.selected_assign.name}/${this.$session.get('user')}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.questions = res.data.questions;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSelectedQuestion(questionName) {
      const result = this.questions.filter((q) => q.name === questionName);
      if (result !== []) {
        [this.selected_question] = result;
      }
    },
    getParts() {
      const path = `http://localhost:5000/student/parts/${this.selected_assign.name}/${this.selected_question.name}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.parts = res.data.parts;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSelectedPart(partNum) {
      const result = this.parts.filter((p) => p.part_num === partNum);
      if (result !== []) {
        [this.selected_part] = result;
      }
    },
    getAnswerStatus() {
      const path = `http://localhost:5000/student/answers/${this.selected_assign.name}/${this.selected_question.name}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          console.log(res.data.answers);
          this.grades = res.data.answers;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getAnswer() {
      const path = `http://localhost:5000/student/answer/${this.selected_assign.name}/${this.selected_question.name}/${this.selected_part.part_num}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          console.log(res.data.answer);
          this.selected_answer = res.data.answer;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    submitAnswer() {
      const path = `http://localhost:5000/student/answer/${this.selected_assign.name}/${this.selected_question.name}/${this.selected_part.part_num}`;
      axios.patch(path, { answer: this.selected_answer.response }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    console.log(this.$session.get('user'));
    if (this.$session.get('user') === undefined) {
      this.$router.push('/login?unauthorized=true');
    }
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.getAssignments();
  },
};
</script>
