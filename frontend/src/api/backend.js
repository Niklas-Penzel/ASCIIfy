import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export default {
  async asciify(formData) {
    const response = await axios.post(`${API_URL}/api/asciify`, formData);
    let asciifiedImageURL = "data:img/jpeg;base64," + response.data;
    return asciifiedImageURL;
  },
  async getFonts() {
    const response = await axios.get(`${API_URL}/api/fonts`);
    let fonts = response.data["fonts"];
    return fonts;
  },
};
