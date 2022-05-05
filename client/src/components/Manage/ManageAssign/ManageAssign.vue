<template>
  <div>
    <div v-show="showComponent === 'default'" class='container'>
      <div class='row'>
        <button @click="$parent.showComp = 'manage_home';"
          class="mr-4 mb-2 btn btn-secondary">
          &laquo; Back
        </button>
        <h3 class='mr-2'> <b> Assignment: </b> {{ this.selected_assign.name}} </h3>
        <h3 class='mr-2' v-if="selected_question.name != ''" >
          <b> Question: </b> {{ this.selected_question.name}}
        </h3>
        <h3 v-if="selected_part.part_num != ''" >
          <b> Part: </b> {{ this.selected_part.part_num}}
        </h3>
      </div>
      <div class='row'>
        <b-dropdown id="assign-drop" text="Select Assignment" class="mr-2 my-2">
        <b-dropdown-item v-for="assign in assignments" v-bind:key="assign.name"
        @click="getSelectedAssignment(assign.name); selected_assign.name = assign.name;
        selected_question = { name: '', format: '' }; getQuestions();">
          {{ assign.name }} </b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item v-b-modal.add-assign-modal> Add Assignment</b-dropdown-item>
        <b-dropdown-item v-b-modal.rem-assign-modal> Delete Assignment</b-dropdown-item>
        </b-dropdown>
        <div class='btn-group btn-group m-2' v-if="selected_assign.name != ''">
          <button type="button" :class=
          "selected_assign.published ? 'btn btn-success' : 'btn btn-danger'"
          @click="toggleAssignPublished();">
          Published</button>
          <button type="button"
            :class= "selected_assign.active?'btn btn-success':'btn btn-danger'"
            @click="toggleAssignActive();">
            Active
          </button>
          <button type="button"
            :class= "selected_assign.exam?'btn btn-success':'btn btn-danger'"
            @click="toggleAssignExam();">
            Exam
          </button>
        </div>
      </div>
      <div class='row'>
        <b-dropdown v-if="selected_assign.name != ''" id="question-drop" text="Select Question"
        class="mr-2 my-2">
        <b-dropdown-item v-for="question in questions" v-bind:key="question.name"
        @click="getSelectedQuestion(question.name); selected_question.name = question.name;
        selected_part = { part_num: '', direction: '' }; getParts();">
          {{ question.name }} </b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item v-b-modal.add-question-modal> Add Question</b-dropdown-item>
        <b-dropdown-item v-b-modal.rem-question-modal> Delete Question</b-dropdown-item>
        </b-dropdown>
        <div class='btn-group btn-group m-md-2' v-if="selected_question.name != ''">
          <button type="button"
          @click="showComponent = 'format'"
            class="btn btn-secondary">Format
          </button>
          <button type="button" class="btn btn-secondary"
          @click="showComponent = 'params'">
          Params</button>
        </div>
      </div>
      <div class='row'>
        <b-dropdown v-if="selected_question.name != ''" id="part-drop" text="Select Part"
        class="mr-4 my-2">
        <b-dropdown-item v-for="part in parts" v-bind:key="part.part_num"
        @click="getSelectedPart(part.part_num)">
          {{ part.part_num }} </b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item @click="addPart();"> Add Part</b-dropdown-item>
        </b-dropdown>
        <div class='row' v-if="selected_part.part_num != ''">
          <div class='btn-group m-2 float-right'>
            <button type="button"
            @click="showComponent = 'direction'"
            class="btn btn-secondary">Direction</button>
            <button type="button"
            @click="showComponent = 'rule'"
            class="btn btn-secondary">Grading</button>
          </div>
          <b-dropdown v-if="selected_question.name != ''" id="part-drop" text="Part Order"
          class="my-2">
          <b-dropdown-item v-for="part in parts" v-bind:key="part.part_num"
          @click="setPartOrder(part.part_num); getSelectedPart(part.part_num); getParts()">
            {{ part.part_num }} </b-dropdown-item>
          </b-dropdown>
          <div class='btn-group my-2 ml-2 float-right'>
            <button type="button"
              @click="remPart()"
              class="btn btn-danger"> Delete Part </button>
          </div>
          <div class="col-3 input-group my-2">
            <input @keyup="setPartPoints()" type="number" class="form-control"
            placeholder="Points" v-model="pointVal">
          </div>
        </div>
      </div>
    </div>
    <div v-if="showComponent==='format'" key="key1">
      <ManageAssignFormat />
    </div>
    <div v-if="showComponent==='params'" key="key2">
      <ManageAssignParams />
    </div>
    <div v-if="showComponent==='direction'" key="key2">
      <ManageAssignDirections />
    </div>
    <div v-if="showComponent==='rule'" key="key2">
      <ManageAssignRule />
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
import ManageAssignParams from './ManageAssignParams.vue';
import ManageAssignDirections from './ManageAssignDirections.vue';
import ManageAssignRule from './ManageAssignRule.vue';

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
      selected_assign: { name: '', published: '', active: '' },
      selected_question: { name: '', format: '' },
      selected_part: { part_num: '', direction: '', grading_rule: '' },
      assignments: [],
      questions: [],
      parts: [],
      showComponent: 'default',
      pointVal: '',
    };
  },
  components: {
    ManageAssignFormat,
    ManageAssignParams,
    ManageAssignDirections,
    ManageAssignRule,
  },
  computed: {
    console: () => console,
    window: () => window,
  },
  methods: {
    onAssignSubmit(evt) {
      evt.preventDefault();
      this.$refs.addAssignModal.hide();
      this.addAssignment(this.addAssignForm.name);
      this.initAssignForm();
    },
    initAssignForm() {
      this.addAssignForm.name = '';
    },
    addAssignment(assignName) {
      const path = `http://localhost:5000/assign/${assignName}`;
      axios.post(path, { }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.getAssignments();
          this.getSelectedAssignment(assignName);
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
      this.remAssignment(this.remAssignForm.name);
      this.remAssignForm.name = '';
    },
    remAssignment(assignName) {
      const path = `http://localhost:5000/assign/${assignName}`;
      axios.delete(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.getAssignments();
          this.message = 'Assignment removed';
          this.showMessage = true;
          this.selected_assign = { name: '', published: '', active: '' };
          this.selected_question = { name: '', format: '' };
          this.selected_part = { part_num: '', direction: '', grading_rule: '' };
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
      this.remQuestion(this.selected_assign.name, this.remQuestionForm.name);
      this.remQuestionForm.name = '';
    },
    remQuestion(assignName, questionName) {
      const path = `http://localhost:5000/question/${assignName}/${questionName}`;
      axios.delete(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.getQuestions();
          this.message = 'Question removed';
          this.showMessage = true;
          this.selected_question = '';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getQuestions();
        });
    },
    getAssignments() {
      const path = 'http://localhost:5000/assigns';
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
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
      const path = `http://localhost:5000/assign/${assignmentName}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
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
    toggleAssignPublished() {
      const path = `http://localhost:5000/assign/${this.selected_assign.name}`;
      axios.patch(path, { published: !this.selected_assign.published }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      });
      this.getSelectedAssignment(this.selected_assign.name);
      this.getSelectedAssignment(this.selected_assign.name);
    },
    toggleAssignActive() {
      const path = `http://localhost:5000/assign/${this.selected_assign.name}`;
      axios.patch(path, { active: !this.selected_assign.active }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      });
      // I have to do this twice. No, I do not know why.
      this.getSelectedAssignment(this.selected_assign.name);
      this.getSelectedAssignment(this.selected_assign.name);
    },
    toggleAssignExam() {
      const path = `http://localhost:5000/assign/${this.selected_assign.name}`;
      axios.patch(path, { exam: !this.selected_assign.exam }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      });
      // I have to do this twice. No, I do not know why.
      this.getSelectedAssignment(this.selected_assign.name);
      this.getSelectedAssignment(this.selected_assign.name);
    },
    onQuestionSubmit(evt) {
      evt.preventDefault();
      this.$refs.addQuestionModal.hide();
      this.addQuestion(this.selected_assign.name, this.addQuestionForm.name);
      this.initQuestionForm();
    },
    initQuestionForm() {
      this.addQuestionForm.name = '';
    },
    addQuestion(assignName, questionName) {
      const path = `http://localhost:5000/question/${assignName}/${questionName}`;
      axios.post(path, { }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.getQuestions();
          this.message = 'Question added';
          this.showMessage = true;
          this.getSelectedQuestion(questionName);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getQuestions();
        });
    },
    getQuestions() {
      const path = `http://localhost:5000/questions/${this.selected_assign.name}`;
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
      const path = `http://localhost:5000/question/${this.selected_assign.name}/${questionName}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.selected_part = { part_num: '', direction: '', grading_rule: '' };
          this.selected_question = res.data.question;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getParts() {
      const path = `http://localhost:5000/parts/${this.selected_assign.name}/${this.selected_question.name}`;
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
      const path = `http://localhost:5000/part/${this.selected_assign.name}/${this.selected_question.name}/${partNum}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.selected_part = res.data.part;
          this.pointVal = res.data.part.point_val;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addPart() {
      const path = `http://localhost:5000/part/${this.selected_assign.name}/${this.selected_question.name}/0`;
      axios.post(path, { }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.message = 'Part added';
          this.showMessage = true;
          this.getParts();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
      this.getParts();
    },
    remPart() {
      const path = `http://localhost:5000/part/${this.selected_assign.name}/${this.selected_question.name}/${this.selected_part.part_num}`;
      axios.delete(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.message = 'Part deleted';
          this.showMessage = true;
          this.selected_part = { part_num: '', direction: '', grading_rule: '' };
          this.getParts();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    setPartOrder(partOrder) {
      const path = `http://localhost:5000/part/${this.selected_assign.name}/${this.selected_question.name}/${this.selected_part.part_num}`;
      axios.patch(path, { part_order: partOrder }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.message = 'Part changed';
          this.showMessage = true;
          this.getParts();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    setPartPoints() {
      const path = `http://localhost:5000/part/${this.selected_assign.name}/${this.selected_question.name}/${this.selected_part.part_num}`;
      axios.patch(path, { point_val: this.pointVal }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.message = 'Part changed';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
  },
  created() {
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.getAssignments();
  },
};

</script>
