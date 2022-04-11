<template>
  <div>
    <div class="row pb-3 px-3">
      <button @click="$parent.showComponent = 'default'"
      class="col- btn btn-secondary">
      &laquo; Back
      </button>
      <button @click="submitFormat(); $parent.selected_question.format = format;"
      class="col- btn btn-success ml-2">
      Save
      </button>
    </div>
    <div class="row">
      <div class="col-8 form-group">
          <textarea v-model="format" class="form-control"
          id="exampleFormControlTextarea1" rows="15"></textarea>
      </div>
      <div class="col">
          <div v-html="format"></div>
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
      axios.patch(path, {
        params: {
          token: 'test token',
          format: this.format,
        },
      });
    },
  },
  mounted() {
    console.log('Update');
    this.format = this.$parent.selected_question.format;
  },
};
</script>
