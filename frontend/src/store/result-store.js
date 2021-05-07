import { GenericStore } from "./index";
import backend from "../api/backend";

class ResultStore extends GenericStore {
  data() {
    return {
      asciifiedImageURL: "",
    };
  }
  async setAsciifiedImageURL(file) {
    var data = new FormData();
    data.append("image", file);
    data.append("fontsize", 10);
    data.append("font", "Cousine-Regular");
    data.append("resize", -1);
    this.state.asciifiedImageURL = await backend.asciify(data);
  }
}
export const resultStore = new ResultStore();
