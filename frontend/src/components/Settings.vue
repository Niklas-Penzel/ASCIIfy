<template>
  <div class="settings">
    <h1>Settings</h1>
    <v-divider></v-divider>
    <h2>Fonts</h2>
    <select-option
      class="select-option"
      v-model="currentFont"
      :values="fonts"
      default="Select Font"
    />
    <v-divider></v-divider>
    <h2>Styles</h2>
    <select-option
      class="select-option"
      v-model="currentStyle"
      :values="styles"
      default="Select Style"
    />
    <v-divider></v-divider>
    <div class="slider-option">
      <h2>Font Size</h2>
      <slider v-model="fontSize" :min="10" :max="100" :tooltip="true" />
    </div>
    <v-divider class="slider-divider"></v-divider>
    <h2>Resolution</h2>
    <boolean-option class="boolean-option" v-model="changeResolution" />
    <slider v-if="changeResolution" v-model="resize" :min="1" />
  </div>
</template>

<script>
import BooleanOption from "./BooleanOption";
import Slider from "@vueform/slider";
import { ref, onMounted, computed } from "vue";
import SelectOption from "./SelectOption.vue";
import backend from "../api/backend";
import { resultStore } from "../store/result-store";

export default {
  name: "Settings",
  components: {
    BooleanOption,
    Slider,
    SelectOption,
  },
  setup() {
    const fonts = ref([]);
    const styles = ref([]);

    const currentFont = computed({
      get: () => {
        return resultStore.getState().currentFont;
      },
      set: (value) => {
        resultStore.setSetting("currentFont", value);
      },
    });

    const currentStyle = computed({
      get: () => {
        return resultStore.getState().currentStyle;
      },
      set: (value) => {
        resultStore.setSetting("currentStyle", value);
      },
    });

    const fontSize = computed({
      get: () => {
        return resultStore.getState().fontSize;
      },
      set: (value) => {
        resultStore.setSetting("fontSize", value);
      },
    });

    const resize = computed({
      get: () => {
        return resultStore.getState().resize;
      },
      set: (value) => {
        resultStore.setSetting("resize", value);
      },
    });

    const changeResolution = computed({
      get: () => {
        return resultStore.getState().changeResolution;
      },
      set: (value) => {
        resultStore.setSetting("changeResolution", value);
      },
    });

    onMounted(() => {
      backend.getFonts().then((data) => {
        fonts.value = data;
      });
      backend.getStyles().then((data) => {
        styles.value = data;
      });
    });
    return {
      resize,
      fontSize,
      changeResolution,
      fonts,
      currentFont,
      styles,
      currentStyle,
    };
  },
};
</script>
<style src="@vueform/slider/themes/default.css"></style>
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

h1,
h2 {
  color: #003322;
}
</style>