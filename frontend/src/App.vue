<template>
  <v-app>
    <v-main>
      <HelloWorld />
      <drag-and-drop />
    </v-main>
  </v-app>
</template>

<script>
import DragAndDrop from "./components/DragAndDrop.vue";
import HelloWorld from "./components/HelloWorld.vue";

export default {
  name: "App",

  components: {
    HelloWorld,
    DragAndDrop,
  },
};
</script>

<style>
:root {
  --background-base: #e5edf1;
  --primary-base: #009966;
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
</style>
