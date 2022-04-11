<template>
  <div>
    <div v-show="showComponent === 'default'" class='container'>
      <div class='row align-items-start'>
        <h3 class='col-md' v-if="selected_assign.name === ''"> Assignment </h3>
        <h3 v-else class='col-4 mr-3'> Assignment: {{ this.selected_assign.name}} </h3>
        <h3 class='col-4' v-if="selected_question.name != ''">
          Question: {{ this.selected_question.name}}
        </h3>
        <button @click="$parent.showComp = 'manage_home';"
          class="col- btn btn-secondary">
          &laquo; Back
        </button>
      </div>
      <div class='row'>
        <b-dropdown id="assign-drop" text="Select Assignment" class="m-md-2">
        <b-dropdown-item v-for="assign in assignments" v-bind:key="assign.name"
        @click="getSelectedAssignment(assign.name); selected_question = { name: '', format: '' };
        getQuestions(assign.name);">
          {{ assign.name }} </b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item v-b-modal.add-assign-modal> Add Assignment</b-dropdown-item>
        <b-dropdown-item v-b-modal.rem-assign-modal> Delete Assignment</b-dropdown-item>
        </b-dropdown>
        <div class='btn-group btn-group m-md-2' v-if="selected_assign.name != ''">
          <button type="button" :class=
          "selected_assign.published ? 'btn btn-success' : 'btn btn-danger'"
          @click="toggleAssignPublished();">
          Published</button>
          <button type="button"
            :class= "selected_assign.active?'btn btn-success':'btn btn-danger'"
            @click="toggleAssignActive();">
            Active
          </button>
        </div>
      </div>
      <div class='row'>
        <b-dropdown v-if="selected_assign.name != ''" id="question-drop" text="Select Question"
        class="m-md-2">
        <b-dropdown-item v-for="question in questions" v-bind:key="question.name"
        @click="getSelectedQuestion(question.name)">
          {{ question.name }} </b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item v-b-modal.add-question-modal> Add Question</b-dropdown-item>
        <b-dropdown-item v-b-modal.rem-question-modal> Delete Question</b-dropdown-item>
        </b-dropdown>
        <div class='btn-group btn-group m-md-2' v-if="selected_question.name != ''">
          <button type="button"
          @click="getSelectedQuestion(selected_question.name); showComponent = 'format'"
            class="btn btn-secondary">Format
          </button>
          <button type="button" class="btn btn-secondary">Params</button>
        </div>
      </div>
      <div class='row'>
        <b-dropdown v-if="selected_question.name != ''" id="part-drop" text="Select Part"
        class="m-md-2">
        <b-dropdown-item v-for="part in parts" v-bind:key="part.part_num"
        @click="selected_part=part.part_num">
          {{ part.part_num }} </b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item @click="addPart()"> Add Part</b-dropdown-item>
        <b-dropdown-item v-b-modal.rem-part-modal> Delete Part</b-dropdown-item>
        </b-dropdown>
        <div class='btn-group btn-group m-md-2 float-right' v-if="selected_part != ''">
          <button type="button" class="btn btn-secondary">Direction</button>
          <button type="button" class="btn btn-secondary">Grading Rule</button>
        </div>
      </div>
    </div>
    <div v-if="showComponent==='format'" key="key">
      <ManageAssignFormat />
    </div>
    <b-modal ref="addAssignModal"
            id="add-assign-modal"
            title="Add a new Assignment"
            hide-footer>
      <b-form @submit="onAssignSubmit" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addAssignForm.name"
                        required
                        placeholder="Enter Assignment Name">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="addQuestionModal"
            id="add-question-modal"
            title="Add a new Question"
            hide-footer>
      <b-form @submit="onQuestionSubmit" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addQuestionForm.name"
                        required
                        placeholder="Enter Question Name">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="remAssignModal"
            id="rem-assign-modal"
            title="Removes an assignment"
            hide-footer>
      <b-form @submit="onRemAssignSubmit" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="remAssignForm.name"
                        required
                        placeholder="Enter Assignment Name">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="remQuestionModal"
            id="rem-question-modal"
            title="Removes a question"
            hide-footer>
      <b-form @submit="onRemQuestionSubmit" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="remQuestionForm.name"
                        required
                        placeholder="Enter Question Name">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<style scoped>
  .nowrap {
    white-space: nowrap;
  }
</style>

<script>
import Vue from 'vue';
import VueSessionStorage from 'vue-sessionstorage';
import axios from 'axios';
import ManageAssignFormat from './ManageAssignFormat.vue';

Vue.use(VueSessionStorage);
Vue.config.productionTip = false;

export default {
  data() {
    return {
      addAssignForm: {
        name: '',
      },
      addQuestionForm: {
        name: '',
      },
      remAssignForm: {
        name: '',
      },
      remQuestionForm: {
        name: '',
      },
      assignments: [],
      selected_assign: { name: '', published: '', active: '' },
      selected_question: { name: '', format: '' },
      selected_part: '',
      questions: [],
      parts: [],
      showComponent: 'default',
    };
  },
  components: {
    ManageAssignFormat,
  },
  computed: {
    console: () => console,
    window: () => window,
  },
  methods: {
    onAssignSubmit(evt) {
      evt.preventDefault();
      this.$refs.addAssignModal.hide();
      const payload = { token: 'test token' };
      this.addAssignment(this.addAssignForm.name, payload);
      this.initAssignForm();
    },
    initAssignForm() {
      this.addAssignForm.name = '';
    },
    addAssignment(assignName, payload) {
      const path = `http://localhost:5000/assign/${assignName}`;
      axios.post(path, payload)
        .then(() => {
          this.getAssignments();
          this.getSelectedAssignment(assignName);
          this.getQuestions(this.selected_assign.name);
          this.message = 'Assignment added';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAssignments();
        });
    },
    onRemAssignSubmit(evt) {
      evt.preventDefault();
      this.$refs.remAssignModal.hide();
      const payload = {
        token: 'test token',
      };
      this.remAssignment(this.remAssignForm.name, payload);
      this.remAssignForm.name = '';
    },
    remAssignment(assignName, payload) {
      const path = `http://localhost:5000/assign/${assignName}`;
      axios.delete(path, payload)
        .then(() => {
          this.getAssignments();
          this.message = 'Assignment removed';
          this.showMessage = true;
          this.selected_assign = { name: '', published: '', active: '' };
          this.selected_question = { name: '', format: '' };
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAssignments();
        });
    },
    onRemQuestionSubmit(evt) {
      evt.preventDefault();
      this.$refs.remQuestionModal.hide();
      const payload = {
        token: 'test token',
      };
      this.remQuestion(this.selected_assign.name, this.remQuestionForm.name, payload);
      this.remQuestionForm.name = '';
    },
    remQuestion(assignName, questionName, payload) {
      const path = `http://localhost:5000/question/${assignName}/${questionName}`;
      axios.delete(path, { data: payload })
        .then(() => {
          this.getQuestions(this.selected_assign.name);
          this.message = 'Question removed';
          this.showMessage = true;
          this.selected_question = '';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getQuestions(this.selected_assign.name);
        });
    },
    getAssignments() {
      const path = 'http://localhost:5000/assigns';
      axios.get(path, {
        params: {
          token: 'test token',
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
      const path = `http://localhost:5000/assign/${assignmentName}`;
      console.log(assignmentName);
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          console.log(res.data.assignment);
          this.selected_assign = res.data.assignment;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    toggleAssignPublished() {
      const path = `http://localhost:5000/assign/${this.selected_assign.name}`;
      axios.patch(path, {
        params: {
          token: 'test token',
          published: !this.selected_assign.published,
        },
      });
      this.getSelectedAssignment(this.selected_assign.name);
      this.getSelectedAssignment(this.selected_assign.name);
    },
    toggleAssignActive() {
      const path = `http://localhost:5000/assign/${this.selected_assign.name}`;
      axios.patch(path, {
        params: {
          token: 'test token',
          active: !this.selected_assign.active,
        },
      });
      // I have to do this twice. No, I do not know why.
      this.getSelectedAssignment(this.selected_assign.name);
      this.getSelectedAssignment(this.selected_assign.name);
    },
    onQuestionSubmit(evt) {
      evt.preventDefault();
      this.$refs.addQuestionModal.hide();
      const payload = { token: 'test token' };
      this.addQuestion(this.selected_assign.name, this.addQuestionForm.name, payload);
      this.initQuestionForm();
    },
    initQuestionForm() {
      this.addQuestionForm.name = '';
    },
    addQuestion(assignName, questionName, payload) {
      const path = `http://localhost:5000/question/${assignName}/${questionName}`;
      axios.post(path, payload)
        .then(() => {
          this.getQuestions(this.selected_assign.name);
          this.message = 'Question added';
          this.showMessage = true;
          this.getSelectedQuestion(questionName);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getQuestions(this.selected_assign.name);
        });
    },
    getQuestions(assignName) {
      const path = `http://localhost:5000/questions/${assignName}`;
      axios.get(path, {
        params: {
          token: 'test token',
          assignName: this.selected_assign.name,
        },
      })
        .then((res) => {
          this.questions = res.data.questions;
          console.log(this.questions);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSelectedQuestion(questionName) {
      const path = `http://localhost:5000/question/${this.selected_assign.name}/${questionName}`;
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

    },
    addPart() {

    },
  },
  created() {
    this.getAssignments();
  },
};
</script>
