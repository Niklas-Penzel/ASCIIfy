<template>
  <div>
    <HelloWorld />
    <drag-and-drop />
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import DragAndDrop from "./components/DragAndDrop.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
    DragAndDrop,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  display: flex;
  width: 100%;
  align-content: center;
  justify-content: center;
  color: #2c3e50;
  margin-top: 60px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
