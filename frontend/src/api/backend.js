import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export default {
  async asciify(formData) {
    const response = await axios.post(`${API_URL}/api/asciify`, formData);
    let asciifiedImageURL = "data:img/jpeg;base64," + response.data;
    return asciifiedImageURL;
  },
  async artify(formData) {
    const response = await axios.post(`${API_URL}/api/artify`, formData);
    let artifiedImageURL = "data:img/jpeg;base64," + response.data;
    return artifiedImageURL;
  },
  async beautify(formData) {
    const response = await axios.post(`${API_URL}/api/beautify`, formData);
    let beautifiedImageURL = "data:img/jpeg;base64," + response.data;
    return beautifiedImageURL;
  },
  async getFonts() {
    const response = await axios.get(`${API_URL}/api/fonts`);
    let fonts = response.data["fonts"];
    return fonts;
  },
  async getStyles() {
    const response = await axios.get(`${API_URL}/api/styles`);
    let styles = response.data["styles"];
    return styles;
  },
};
