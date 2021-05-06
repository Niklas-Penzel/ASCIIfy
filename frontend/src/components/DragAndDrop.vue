<template>
  <div class="drag-and-drop">
    <div
      class="drag-area"
      @dragover="dragover"
      @dragleave="dragleave"
      @drop="drop"
      :class="{ active: active }"
    >
      <img v-if="fileURL != ''" :src="fileURL" />
      <div v-else class="inner">
        <fa class="icon" icon="cloud-upload-alt" size="6x" />
        <header>{{ dragText }}</header>
        <input ref="fsFileInput" type="file" @change="handleFileChange" />
      </div>
    </div>

    <button @click="$refs.fsFileInput.click()">Choose A File</button>
  </div>
</template>
<script>
import { ref } from "vue";
export default {
  name: "DragAndDrop",
  setup() {
    const file = ref("");
    const fileURL = ref("");
    const dragText = ref("Drag & Drop to Upload File");
    const active = ref(false);

    const handleFileChange = function (event) {
      active.value = true;
      file.value = event.target.files[0];
      showFile();
    };

    const dragover = function (event) {
      event.preventDefault();
      active.value = true;
      dragText.value = "Release to Upload File";
    };
    const dragleave = function () {
      active.value = false;
      dragText.value = "Drag & Drop to Upload File";
    };

    const showFile = function () {
      let fileType = file.value.type;
      let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
      if (!validExtensions.includes(fileType)) {
        alert("This is NOT an Image File");
        active.value = false;
      }
      let fileReader = new FileReader();
      fileReader.onload = () => {
        fileURL.value = fileReader.result;
      };
      fileReader.readAsDataURL(file.value);
    };

    const drop = function (event) {
      event.preventDefault();
      file.value = event.dataTransfer.files[0];
      showFile(event);
    };
    return {
      dragover,
      dragleave,
      drop,
      fileURL,
      dragText,
      handleFileChange,
      active,
    };
  },
};
</script>

<style scoped>
.drag-and-drop {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.drag-area {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #c2cdda;
  height: 300px;
  width: 500px;
  border-radius: 5px;
  flex-direction: column;
}

.drag-area .inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.drag-area.active {
  border: 2px solid #c2cdda;
}

.drag-area .icon {
  color: #29abe2;
}
.drag-area header {
  color: #29abe2;
  font-size: 30px;
  font-weight: 500;
}

.drag-area span {
  color: #29abe2;
  font-size: 25px;
  font-weight: 500;
}

button {
  padding: 10px 25px;
  width: 80%;
  margin-top: 10px;
  font-size: 20px;
  font-weight: 500;
  border: none;
  outline: none;
  background: #29abe2;
  color: black;
  border-radius: 20px;
  cursor: pointer;
}

.drag-area img {
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 3px;
}

.drag-area input {
  display: none;
}
</style>
