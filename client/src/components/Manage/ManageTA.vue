<template>
  <div class="container">
    <div class="row g-10">
        <div class="list-group list-group-flush col-md-6 ml-auto">
            <li class="list-group-item" v-for="ta in TAs" v-bind:key="ta.name">
              {{ ta.name }} ({{ ta.net_id }}) </li>
        </div>
        <div class="col-md-4">
            <div class="btn-group-vertical" role="group">
               <button class = "btn btn-primary btn-md" type="button"
               v-b-modal.ta-modal>Add TA</button>
               <button class = "btn btn-danger btn-md" type="button"
               v-b-modal.remove-modal>Remove TA</button>
            </div>
        </div>
    </div>
    <b-modal ref="addTAModal"
            id="ta-modal"
            title="Add a new TA"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addTAForm.name"
                        required
                        placeholder="Enter Name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-netid-group"
                      label="Net-Id:"
                      label-for="form-netid-input">
            <b-form-input id="form-netid-input"
                          type="text"
                          v-model="addTAForm.net_id"
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
    <b-modal ref="remTAModal"
            id="remove-modal"
            title="Remove a TA"
            hide-footer>
      <b-form @submit="onRemSubmit" @reset="onRemReset" class="w-100">
        <b-form-group id="form-rem-netid-group"
                      label="Net-Id:"
                      label-for="form-rem-netid-input">
            <b-form-input id="form-rem-netid-input"
                          type="text"
                          v-model="remTAForm.net_id"
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

<style>
  .list-group{
      max-height: 300px;
      margin-bottom: 10px;
      overflow:scroll;
      -webkit-overflow-scrolling: touch;
      outline:solid;
  }
</style>

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
      addTAForm: {
        title: '',
        author: '',
        read: [],
      },
      remTAForm: {
        net_id: '',
      },
      message: '',
      showMessage: false,
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
    addTA(payload) {
      const path = 'http://localhost:5000/manage/student';
      axios.post(path, payload)
        .then(() => {
          this.getTAs();
          this.message = 'TA added';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTAs();
        });
    },
    remTA(payload) {
      const path = 'http://localhost:5000/manage/student';
      axios.delete(path, { data: payload })
        .then(() => {
          this.getTAs();
          this.message = 'TA removed';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTAs();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTAModal.hide();
      const payload = {
        name: this.addTAForm.name,
        net_id: this.addTAForm.net_id,
        is_ta: 'True',
        token: 'test token',
      };
      this.addTA(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTAModal.hide();
      this.initForm();
    },
    initForm() {
      this.addTAForm.name = '';
      this.addTAForm.net_id = '';
    },
    onRemSubmit(evt) {
      evt.preventDefault();
      this.$refs.remTAModal.hide();
      const payload = {
        net_id: this.remTAForm.net_id,
        token: 'test token',
      };
      this.remTA(payload);
      this.initForm();
    },
    onRemReset(evt) {
      evt.preventDefault();
      this.$refs.remTAModal.hide();
      this.initRemForm();
    },
    initRemForm() {
      this.remTAForm.net_id = '';
    },
  },
  created() {
    this.getTAs();
  },
};
</script>
