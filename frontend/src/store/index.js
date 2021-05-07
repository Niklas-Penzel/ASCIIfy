import { reactive, readonly } from "vue";

export class GenericStore {
  constructor() {
    let data = this.data();
    this.state = reactive(data);
  }
  getState() {
    return readonly(this.state);
  }
}
