<template>
  <div>
    <div class='row px-3'>
        <h3> Edit Question Params </h3>
    </div>
    <div class="row pb-3 px-3">
        <button @click="$parent.showComponent = 'default'"
        class="col- btn btn-secondary">
        &laquo; Back
        </button>
        <button @click="sampleParamRule()"
        class="col- btn btn-primary ml-2">
        Sample
        </button>
        <button @click="submitParamRule()"
        class="col- btn btn-success ml-2">
        Save
        </button>
    </div>
    <div class="row">
      <div class="col-8 form-group">
        <textarea v-model="paramFunc" class="form-control"
        id="exampleFormControlTextarea1" @keydown.tab.prevent="tabber($event)"
        placeholder='global params
params = ...'
        rows="2"></textarea>
      </div>
    </div>
    <div class="row pb-3 px-3">
      <h4> Sample Output: </h4>
    </div>
    <div class="row pb-3 px-3">
      <p> {{ paramSample }} </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      paramFunc: '',
      paramSample: '',
    };
  },
  methods: {
    submitParamRule() {
      const path = `http://localhost:5000/question/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}`;
      axios.patch(path, {
        params: {
          token: 'test token',
          param_func: this.paramFunc,
        },
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    sampleParamRule() {
      const path = 'http://localhost:5000/sampleparamfunc';
      axios.put(path, {
        params: {
          token: 'test token',
          param_func: this.paramFunc,
        },
      })
        .then((res) => {
          this.paramSample = res.data.param_sample;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    tabber(event) {
      const text = this.paramFunc;
      const originalSelectionStart = event.target.selectionStart;
      const textStart = text.slice(0, originalSelectionStart);
      const textEnd = text.slice(originalSelectionStart);

      this.paramFunc = `${textStart}\t${textEnd}`;
    },
    updateParamFunc(questionName) {
      const path = `http://localhost:5000/question/${this.$parent.selected_assign.name}/${questionName}`;
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.paramFunc = res.data.question.param_func;
          console.log(this.paramFunc);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.updateParamFunc(this.$parent.selected_question.name);
  },
};
</script>
