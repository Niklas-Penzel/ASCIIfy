<template>
  <v-app>
    <v-main>
      <h1 class="logo">ASCIIfy</h1>
      <div class="main-container">
        <settings />
        <drag-and-drop />
      </div>
      <result-display class="result" />
    </v-main>
  </v-app>
</template>

<script>
import DragAndDrop from "./components/DragAndDrop.vue";
import ResultDisplay from "./components/ResultDisplay.vue";
import Settings from "./components/Settings.vue";

export default {
  name: "App",
  components: {
    DragAndDrop,
    ResultDisplay,
    Settings,
  },
  data: () => {
    return { keepResolution: false };
  },
};
</script>

<style>
:root {
  --background-base: #e5edf1;
  --primary-base: #41b883;
  --secondary-base: #003322;
}

.v-application {
  background-color: var(--background-base) !important;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body::-webkit-scrollbar {
  width: 0.5rem;
}
body::-webkit-scrollbar-track {
  background: rgb(14, 192, 124);
}
body::-webkit-scrollbar-thumb {
  background: rgb(15, 124, 82);
}

.main-container {
  display: flex;
  width: 90%;
  margin: auto;
}

.logo {
  font-size: 70px;
  width: 90%;
  text-align: center;
  margin: 0 auto;
  color: #003322;
}

.result {
  margin-top: 10px;
}
</style>
