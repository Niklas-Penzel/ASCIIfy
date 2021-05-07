<template>
  <div class="drag-and-drop">
    <div
      class="drag-area"
      @dragover="dragover"
      @dragleave="dragleave"
      @drop="drop"
      @click="$refs.fsFileInput.click()"
      :class="{ active: active, uploaded: uploaded }"
    >
      <div v-if="fileURL != ''">
        <img :src="fileURL" />
      </div>
      <div v-else class="inner">
        <v-icon class="icon" size="70">fas fa-cloud-upload-alt</v-icon>
        <header>Drag & Drop or Click to Upload File</header>
        <input
          ref="fsFileInput"
          type="file"
          @change.prevent="handleFileChange"
        />
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from "vue";
import { resultStore } from "../store/result-store";
export default {
  name: "DragAndDrop",
  setup() {
    const file = ref("");
    const fileURL = ref("");
    const active = ref(false);
    const uploaded = ref(false);

    const handleFileChange = function (event) {
      active.value = true;
      file.value = event.target.files[0];
      showFile();
      resultStore.setAsciifiedImageURL(file.value);
      uploaded.value = true;
    };

    const dragover = function (event) {
      event.preventDefault();
      active.value = true;
    };
    const dragleave = function () {
      active.value = false;
    };

    const showFile = function () {
      let fileType = file.value.type;
      let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
      if (!validExtensions.includes(fileType)) {
        alert("This is NOT an Image File");
        active.value = false;
      }
      let fileReader = new FileReader();
      fileReader.onload = (event) => {
        fileURL.value = event.target.result;
      };
      fileReader.readAsDataURL(file.value);
    };

    const drop = function (event) {
      event.preventDefault();
      file.value = event.dataTransfer.files[0];
      showFile(event);
      resultStore.setAsciifiedImageURL(file.value);
      uploaded.value = true;
    };
    return {
      dragover,
      dragleave,
      drop,
      fileURL,
      handleFileChange,
      active,
      uploaded,
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
  margin: 0 auto;
  max-width: 520px;
  cursor: pointer;
}

.drag-area {
  display: flex;
  align-items: center;
  justify-content: center;
  outline: 2px dashed #92b0b3;
  flex-direction: column;
  outline-offset: -6px;
  background-color: #c8dadf;
  transition: outline-offset 0.15s ease-in-out, background-color 0.15s linear;
}

.drag-area .inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 50px 100px;
}

.drag-area.active {
  outline-offset: -12px;
  background-color: rgb(250, 250, 250);
}
.drag-area.active.uploaded {
  outline: none;
}

.drag-area .icon {
  color: var(--primary-base);
}
.drag-area header {
  color: var(--primary-base);
  font-size: 20px;
  font-weight: 500;
  margin-top: 10px;
}

button {
  padding: 10px 25px;
  width: 80%;
  margin-top: 10px;
  font-size: 20px;
  font-weight: 500;
  border: none;
  outline: none;
  background: var(--primary-base);
  color: white;
  border-radius: 20px;
  cursor: pointer;
}

.drag-area img {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

.drag-area input {
  display: none;
}
</style>
