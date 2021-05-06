<template>
  <div class="row">
    <div class="column left" style="background-color: #9c0d38">
      <h2 style="color: #ffffff">Settings</h2>
      <Multiselect
        style="color: #ffffff"
        :canDeselect="false"
        v-model="selectedFont"
        :options="fonts"
        :searchable="true"
        ref="fontselector"
        @change="handleFonts"
      />
      <br />
      <br />
      <br />
      <Slider
        v-model="size"
        :min="10"
        :max="100"
        :tooltip="true"
        @change="sendRequest"
      />
      <br />
      <div class="flex">
        <span style="color: #ffffff">Keep Resolution:&nbsp;</span>
        <Toggle v-model="keepRes" @change="handleResize" />
      </div>
      <br />
      <br />
      <Slider
        v-model="resize"
        :disabled="keepRes"
        :min="1"
        @change="handleResizeSlider"
      />
    </div>
    <div class="column right" style="background-color: #077187">
      <UploadImages @change="handleImages" />
      <img :src="asciifiedImage" />
    </div>
  </div>
</template>

<script>
import UploadImages from "vue-upload-drop-images";
import slider from "vue3-slider";
import axios from "axios";
import Multiselect from "@vueform/multiselect";
import Toggle from "@vueform/toggle";
import Slider from "@vueform/slider";

const API_URL = "http://127.0.0.1:5000";

export default {
  components: {
    UploadImages,
    slider,
    Multiselect,
    Toggle,
    Slider,
  },
  methods: {
    handleImages(files) {
      if (files.length > 0) {
        this.file = files[0];
        let reader = new FileReader();
        reader.onload = (e) => {
          this.uploadedImage = e.target.result;
          this.sendRequest();
        };
        reader.readAsDataURL(files[0]);

        this.uploadedImage = files[0];
      } else {
        this.asciifiedImage = "";
        this.uploadedImage = "";
      }
    },
    handleFonts(value) {
      console.log(value);
      if (value != null) {
        this.selectedFont = value;
        this.sendRequest();
      } else {
        this.$refs.fontselector.select(this.selectedFont);
      }
    },
    handleResize(value) {
      if (value) {
        this.keepRes = true;
        this.resizeFactor = -1;
      } else {
        this.keepRes = false;
        this.resizeFactor = this.resize;
      }
      this.sendRequest();
    },
    handleResizeSlider(value) {
      this.resizeFactor = value;
      this.sendRequest();
    },
    loadFonts() {
      var self = this;
      axios
        .get(`${API_URL}/api/fonts`, null)
        .then(function (response) {
          self.fonts = response.data["fonts"];
          if (self.fonts.includes("MajorMonoDisplay-Regular")) {
            self.selectedFont = "MajorMonoDisplay-Regular";
          } else {
            self.selectedFont = response.data["fonts"][0];
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    sendRequest() {
      if (this.uploadedImage != "") {
        var data = new FormData();
        data.append("image", this.file);
        data.append("fontsize", this.size);
        data.append("font", this.selectedFont);
        data.append("resize", this.resizeFactor);
        var self = this;
        axios
          .post(`${API_URL}/api/asciify`, data)
          .then(function (response) {
            if (self.uploadedImage != "") {
              console.log(response);
              self.asciifiedImage = "data:img/jpeg;base64," + response.data;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
  data() {
    return {
      size: 32,
      uploadedImage: "",
      asciifiedImage: "",
      selectedFont: null,
      fonts: [],
      keepRes: true,
      resize: 25,
      resizeFactor: -1,
    };
  },
  created() {
    this.loadFonts();
  },
};
</script>

<style src="@vueform/multiselect/themes/default.css"></style>
<style src="@vueform/toggle/themes/default.css"></style>
<style src="@vueform/slider/themes/default.css"></style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img {
  max-width: 100%;
  max-height: 100%;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
* {
  box-sizing: border-box;
}

.flex {
  display: flex;
}

/* Create two unequal columns that floats next to each other */
.column {
  float: left;
  padding: 10px;
}

.left {
  width: 30%;
}

.right {
  width: 70%;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>
