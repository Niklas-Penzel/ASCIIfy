<template>
  <div>
    <div class="select-box">
      <div class="options-container" :class="{ active: active }">
        <div
          class="option"
          v-for="value in values"
          :key="value"
          @click="setValue(value)"
          :class="{ current: value == modelValue }"
        >
          <input type="radio" class="radio" name="category" :id="value" />
          <label :for="value">{{ value }}</label>
        </div>
      </div>
      <div class="selected" @click="active = !active">
        {{ modelValue }} <v-icon>fas fa-chevron-down</v-icon>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  name: "SelectOption",
  props: {
    values: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: String,
    },
    default: {
      type: String,
      default: "Select",
    },
  },
  setup(props, { emit }) {
    const active = ref(false);
    const setValue = function (value) {
      active.value = false;
      if (value == props.modelValue) {
        emit("update:modelValue", props.default);
      } else {
        emit("update:modelValue", value);
      }
    };
    return { active, setValue };
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

.select-box .option.current {
  background-color: #414b57;
}

.select-box label {
  cursor: pointer;
}

.select-box .option .radio {
  display: none;
}
</style>