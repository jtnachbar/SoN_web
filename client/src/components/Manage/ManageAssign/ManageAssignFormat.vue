<template>
  <div>
    <div class="container-fluid">
      <div class = 'row px-3'>
        <h3> Edit Question Format </h3>
      </div>
      <div class="row pb-3 px-3">
        <button @click="$parent.showComponent = 'default'"
        class="col- btn btn-secondary">
        &laquo; Back
        </button>
        <button @click="submitFormat();
        $parent.getSelectedQuestion($parent.selected_question.name);"
        class="col- btn btn-success ml-2">
        Save
        </button>
      </div>
      <div class="row">
        <div class="col-6 form-group">
            <textarea v-model="format" class="form-control"
            id="exampleFormControlTextarea1" rows="15"
            placeholder='... ${1} ... ${2} ...'></textarea>
        </div>
        <div class="col">
            <div v-html="format"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      format: '',
    };
  },
  methods: {
    submitFormat() {
      const path = `http://localhost:5000/question/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}`;
      axios.patch(path, { format: this.format }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      });
    },
    updateFormat(questionName) {
      const path = `http://localhost:5000/question/${this.$parent.selected_assign.name}/${questionName}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.format = res.data.question.format;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.token = this.$session.get('token');
    this.user = this.$session.get('user');
    this.updateFormat(this.$parent.selected_question.name);
  },
};
</script>
