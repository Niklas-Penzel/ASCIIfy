<template>
  <img class="result" :src="resultState.asciifiedImageURL" />
</template>

<script>
import { resultStore } from "../store/result-store";
export default {
  name: "ResultDisplay",
  setup() {
    const resultState = resultStore.getState();

    return { resultState };
  },
};
</script>

<style scoped>
.result {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
</style>