<template>
  <div class="settings">
    <h1>Settings</h1>
    <v-divider></v-divider>
    <select-option class="select-option" />
    <v-divider></v-divider>
    <div class="slider-option">
      <h2>Size</h2>
      <slider v-model="size" :min="10" :max="100" :tooltip="true" />
    </div>
    <v-divider class="slider-divider"></v-divider>
    <h2>Resolution</h2>
    <boolean-option class="boolean-option" v-model="keepResolution" />
    <slider v-if="keepResolution" v-model="resize" :min="1" />
  </div>
</template>

<script>
import BooleanOption from "./BooleanOption";
import Slider from "@vueform/slider";
import { ref } from "vue";
import SelectOption from "./SelectOption.vue";
export default {
  name: "Settings",
  components: {
    BooleanOption,
    Slider,
    SelectOption,
  },
  setup() {
    const keepResolution = ref(false);
    const resize = ref(25);
    const size = ref(32);
    return { resize, size, keepResolution };
  },
};
</script>
<style scoped>
.settings {
  display: flex;
  flex-direction: column;
  width: 30%;
  margin: 20px;
}
h1 {
  margin: 10px 0;
}
.select-option {
  margin: 10px 5px;
}
.slider-option h2 {
  margin-bottom: 40px;
}
.boolean-option {
  margin-bottom: 50px;
}
.slider-divider {
  margin-top: 10px;
}
</style>