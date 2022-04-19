<template>
  <div>
    <div class="container-fluid">
      <div class = 'row px-3'>
        <h3> Edit Directions </h3>
      </div>
      <div class="row pb-3 px-3">
        <button @click="$parent.showComponent = 'default'"
        class="col- btn btn-secondary">
        &laquo; Back
        </button>
        <button @click="submitDirections();
        $parent.getSelectedPart($parent.selected_part.part_num);"
        class="col- btn btn-success ml-2">
        Save
        </button>
      </div>
      <div class="row">
        <div class="col-12 form-group">
            <textarea v-model="directions" class="form-control"
            id="exampleFormControlTextarea2" rows="3"></textarea>
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
      directions: '',
    };
  },
  methods: {
    submitDirections() {
      const path = `http://localhost:5000/part/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}/${this.$parent.selected_part.part_num}`;
      axios.patch(path, {
        token: 'test token',
        directions: this.directions,
      });
    },
    updateDirections() {
      const path = `http://localhost:5000/part/${this.$parent.selected_assign.name}/${this.$parent.selected_question.name}/${this.$parent.selected_part.part_num}`;
      axios.get(path, {
        params: {
          token: 'test token',
        },
      })
        .then((res) => {
          this.directions = res.data.part.direction;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.updateDirections();
  },
};
</script>
