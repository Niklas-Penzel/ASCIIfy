import { GenericStore } from "./index";
import backend from "../api/backend";

class ResultStore extends GenericStore {
  data() {
    return {
      resultImageURL: "",
      currentFont: "Select Font",
      currentStyle: "Select Style",
      changeResolution: false,
      resize: 1,
      fontSize: 10,
      file: null,
    };
  }

  setSetting(key, value) {
    this.state[key] = value;
    if (this.state.file) {
      this.getResultImageURL();
    }
  }
  getSetting(key) {
    return this.state[key];
  }

  setFile(file) {
    this.state.file = file;
  }

  async getResultImageURL() {
    if (
      this.state.currentFont == "Select Font" &&
      this.state.currentStyle == "Select Style"
    ) {
      return;
    }
    const resize = this.state.changeResolution ? this.state.resize : -1;
    var data = new FormData();
    data.append("image", this.state.file);
    data.append("fontsize", this.state.fontSize);
    data.append("resize", resize);
    if (this.state.currentFont != "Select Font") {
      data.append("font", this.state.currentFont.toLowerCase());
    }
    if (this.state.currentStyle != "Select Style") {
      data.append("style", this.state.currentStyle.toLowerCase());
    }
    this.state.resultImageURL = await backend.beautify(data);
  }
}
export const resultStore = new ResultStore();
