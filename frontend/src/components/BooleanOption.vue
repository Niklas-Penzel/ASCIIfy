<template>
  <div class="container">
    <h2>{{ title }}</h2>
    <v-row class="mx-auto" dense>
      <v-col class="col-6">
        <v-sheet
          class="text-center d-flex align-center justify-space-between py-3 px-4"
          rounded
          :color="modelValue ? '#41b883' : '#53565d'"
          flat
          link
          @click="(event) => $emit('update:modelValue', true)"
        >
          <span>Enabled</span><v-icon color="#f5f6fa">fas fa-check</v-icon>
        </v-sheet>
      </v-col>
      <v-col class="col-6">
        <v-sheet
          class="text-center d-flex align-center justify-space-between py-3 px-4"
          rounded
          :color="!modelValue ? '#41b883' : '#53565d'"
          flat
          link
          @click="(event) => $emit('update:modelValue', false)"
        >
          <span>Disabled</span><v-icon color="#f5f6fa">fas fa-times</v-icon>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      default: "",
      type: String,
    },
    name: String,
    modelValue: {
      default: false,
      type: Boolean,
    },
  },
};
</script>

<style scoped>
.v-sheet {
  cursor: pointer;
  color: #f5f6fa;
}
</style>