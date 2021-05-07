<template>
  <div>
    <div class="select-box">
      <div v-if="fonts" class="options-container" :class="{ active: active }">
        <div
          class="option"
          v-for="font in fonts"
          :key="font"
          @click="setFont(font)"
        >
          <input type="radio" class="radio" name="category" :id="font" />
          <label for="test-font1">{{ font }}</label>
        </div>
      </div>
      <div class="selected" @click="active = !active">
        {{ currentFont }} <v-icon>fas fa-chevron-down</v-icon>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import backend from "../api/backend";
export default {
  name: "SelectOption",
  setup() {
    const fonts = ref([]);
    const active = ref(false);
    const currentFont = ref("Select Font");

    onMounted(() => {
      backend.getFonts().then((data) => {
        fonts.value = data;
        if (fonts.value.includes("MajorMonoDisplay-Regular")) {
          currentFont.value = "MajorMonoDisplay-Regular";
        } else {
          currentFont.value = data[0];
        }
      });
    });

    const setFont = function (font) {
      currentFont.value = font;
      active.value = false;
    };

    return { fonts, active, setFont, currentFont };
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
  padding: 32px;
}
.select-box {
  display: flex;
  width: 100%;
  flex-direction: column;
}
.select-box .options-container {
  background-color: #2f3640;
  color: #f5f6fa;
  width: 100%;
  max-height: 0;
  opacity: 0;
  transition: all 0.4s;
  border-radius: 8px;
  overflow: hidden;
  order: 1;
}

.selected {
  background-color: #2f3640;
  border-radius: 8px;
  margin-bottom: 8px;
  color: #f5f6fa;
  position: relative;
  order: 0;
  display: flex;
}

.selected::after {
  content: "";
  background-size: contain;
  background-repeat: no-repeat;
}

.select-box .options-container.active {
  max-height: 240px;
  opacity: 1;
  overflow-y: scroll;
}
.selected i {
  color: #f5f6fa;
  margin-left: auto;
}

.select-box .options-container.active + .selected i {
  transform: rotate(-180deg);
}

.select-box .options-container::-webkit-scrollbar {
  width: 8px;
  background-color: #0d141f;
  border-radius: 0 8px 8px 0;
}
.select-box .options-container::-webkit-scrollbar-thumb {
  background-color: #525861;
  border-radius: 0 8px 8px 0;
}
.select-box .option,
.selected {
  padding: 12px 24px;
  cursor: pointer;
}

.select-box .option:hover {
  background-color: #414b57;
}

.select-box label {
  cursor: pointer;
}

.select-box .option .radio {
  display: none;
}
</style>