<template>
  <div class="container">
    <div class="row g-10">
        <button @click="$parent.showComp = 'manage_home';"
          class="btn btn-secondary float-top float-left">
          &laquo; Back
        </button>
        <div class="list-group list-group-flush col-md-6 ml-auto">
            <li class="list-group-item"
            v-for="student in filteredStudents" v-bind:key="student.name">
              {{ student.name }} ({{ student.net_id }}) </li>
        </div>
        <div class="col-md-4">
            <div class="search-wrapper">
                <input type="text" v-model="search" placeholder="Search Student"/>
            </div>
            <br>
            <div class="btn-group-vertical" role="group">
               <button class = "btn btn-primary btn-md" type="button"
               v-b-modal.student-modal>Add Student</button>
               <button class = "btn btn-danger btn-md" type="button"
               v-b-modal.remove-modal>Remove Student</button>
               <button class = "btn btn-success btn-md" type="button"
               v-b-modal.remove-modal>Add CSV</button>
            </div>
        </div>
    </div>
    <b-modal ref="addStudentModal"
            id="student-modal"
            title="Add a new Student"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addStudentForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-netid-group"
                      label="Net-Id:"
                      label-for="form-netid-input">
            <b-form-input id="form-netid-input"
                          type="text"
                          v-model="addStudentForm.net_id"
                          required
                          placeholder="Enter Net-Id">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="remStudentModal"
            id="remove-modal"
            title="Remove a Student"
            hide-footer>
      <b-form @submit="onRemSubmit" @reset="onRemReset" class="w-100">
        <b-form-group id="form-rem-netid-group"
                      label="Net-Id:"
                      label-for="form-rem-netid-input">
            <b-form-input id="form-rem-netid-input"
                          type="text"
                          v-model="remStudentForm.net_id"
                          required
                          placeholder="Enter Net-Id">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
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
      students: [],
      search: '',
      addStudentForm: {
        title: '',
        author: '',
        read: [],
      },
      remStudentForm: {
        net_id: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
  },
  computed: {
    filteredStudents() {
      return this.students.filter((student) => (
        student.name.toLowerCase().indexOf(this.search.toLowerCase()) > -1
      ));
    },
  },
  methods: {
    getStudents() {
      const path = 'http://localhost:5000/manage/student';
      axios.get(path, {
        params: {
          get_ta: '',
        },
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.students = res.data.students;
          console.log(this.students);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addStudent(payload) {
      const path = 'http://localhost:5000/manage/student';
      axios.post(path, payload, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.getStudents();
          this.message = 'Student added';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getStudents();
        });
    },
    remStudent(payload) {
      const path = 'http://localhost:5000/manage/student';
      axios.delete(path, {
        data: payload,
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then(() => {
          this.getStudents();
          this.message = 'Student removed';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getStudents();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addStudentModal.hide();
      const payload = {
        name: this.addStudentForm.name,
        net_id: this.addStudentForm.net_id,
        is_ta: '',
        token: 'test token',
      };
      this.addStudent(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addStudentModal.hide();
      this.initForm();
    },
    initForm() {
      this.addStudentForm.name = '';
      this.addStudentForm.net_id = '';
    },
    onRemSubmit(evt) {
      evt.preventDefault();
      this.$refs.remStudentModal.hide();
      const payload = {
        net_id: this.remStudentForm.net_id,
        token: 'test token',
      };
      this.remStudent(payload);
      this.initForm();
    },
    onRemReset(evt) {
      evt.preventDefault();
      this.$refs.remStudentModal.hide();
      this.initRemForm();
    },
    initRemForm() {
      this.remStudentForm.net_id = '';
    },
  },
  created() {
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.getStudents();
  },
};
</script>
