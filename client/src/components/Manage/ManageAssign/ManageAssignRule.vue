<template>
  <div>
    <div class='row px-3'>
        <h3> Edit Grading Rule </h3>
    </div>
    <div class="row">
      <div class="col-12 form-group mx-3">
        <div class="row pb-3">
          <button @click="$parent.showComponent = 'default'"
          class="col- btn btn-secondary">
          &laquo; Back
          </button>
          <button @click="sampleGradingRule()"
          class="col- btn btn-primary ml-2">
          Test
          </button>
          <button @click="submitGradingRule()"
          class="col- btn btn-success ml-2">
          Save
          </button>
        </div>
        <div class="row mb-2">
          <textarea v-model="gradingRule" class="col-5 form-control"
          id="exampleFormControlTextarea1" @keydown.tab.prevent="tabber($event)"
          placeholder='if ${s} ... ${1} ${2} ... :
          test_res = true'
          rows="4"></textarea>
          <div class="col-5">
            <b-form-input v-model="testAns" class="mb-1" size="sm" placeholder="Student Answer">
            </b-form-input>
            <b-input-group v-for="n in paramNum" :key="n" class="mb-1" size="sm">
              <b-form-input v-model="paramList[n-1]" :placeholder="'Param ' + n">
                </b-form-input></b-input-group>
          </div>
        </div>
        <div class="row pb-3" v-if="testRes != ''">
          <h4> Sample Output: {{ testRes }} </h4>
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
      gradingRule: '',
      testRes: '',
      paramNum: 0,
      paramList: [],
      testAns: '',
    };
  },
  methods: {
    submitGradingRule() {
      const path = `http://localhost:5000/part/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}/${this.$parent.selected_part.part_num}`;
      axios.patch(path, { grading_rule: this.gradingRule }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    sampleGradingRule() {
      const path = 'http://localhost:5000/samplegradingrule';
      axios.put(path, {
        grading_rule: this.gradingRule,
        params: this.paramList,
        test_ans: this.testAns,
      }, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.testRes = res.data.test_res;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    tabber(event) {
      const text = this.gradingRule;
      const originalSelectionStart = event.target.selectionStart;
      const textStart = text.slice(0, originalSelectionStart);
      const textEnd = text.slice(originalSelectionStart);

      this.gradingRule = `${textStart}\t${textEnd}`;
    },
    updateGradingRule() {
      const path = `http://localhost:5000/part/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}/${this.$parent.selected_part.part_num}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.gradingRule = res.data.part.grading_rule;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateParamNum() {
      const path = `http://localhost:5000/question/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}`;
      axios.get(path, {
        headers: {
          Authorization: `${this.token}`,
          Net_Id: `${this.user}`,
        },
      })
        .then((res) => {
          this.paramNum = res.data.question.param_num;
          for (let i = 0; i < this.paramNum; i += 1) {
            this.paramList[i] = '';
          }
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
    this.updateGradingRule();
    this.updateParamNum();
  },
};
</script>
