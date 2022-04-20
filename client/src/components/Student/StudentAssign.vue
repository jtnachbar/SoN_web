<template>
  <div class="container-lg border-top border-bottom rounded py-2">
    <button
        type="button"
        class="btn btn-success btn-md float-right"
        @click="login()">
        <div v-if="this.$session.get('user') != undefined">
          {{ this.$session.get('user') }}
        </div>
        <div v-else>
          Login
        </div>
    </button>
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
        selected_part = { part_num: '', direction: '' }; getParts();">
          {{ question.name }} </b-dropdown-item>
        </b-dropdown>

        <b-dropdown v-if="selected_question.name != ''" id="part-drop" text="Select Part"
        class="mr-4 my-2">
        <b-dropdown-item v-for="part in parts" v-bind:key="part.part_num"
        @click="getSelectedPart(part.part_num)">
          {{ part.part_num }} </b-dropdown-item>
        </b-dropdown>
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
      assignments: [],
      questions: [],
      parts: [],
    };
  },
  components: {
  },
  methods: {
    getAssignments() {
      const path = 'http://localhost:5000/student/assigns';
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.assignments = res.data.assignments;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSelectedAssignment(assignmentName) {
      const path = `http://localhost:5000/student/assign/${assignmentName}`;
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.selected_assign = res.data.assignment;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getQuestions() {
      const path = `http://localhost:5000/student/questions/${this.selected_assign.name}`;
      axios.get(path, {
        params: {
          token: 'test token',
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
      const path = `http://localhost:5000/student/question/${this.selected_assign.name}/${questionName}`;
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.selected_question = res.data.question;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getParts() {
      const path = `http://localhost:5000/student/parts/${this.selected_assign.name}/${this.selected_question.name}`;
      axios.get(path, {
        params: {
          token: 'test token',
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
      const path = `http://localhost:5000/student/part/${this.selected_assign.name}/${this.selected_question.name}/${partNum}`;
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.selected_part = res.data.part;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getParams() {
      const path = `http://localhost:5000/student/params/${this.selected_assign.name}/${this.selected_question.name}`;
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.params = res.data.params;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getAssignments();
  },
};
</script>
