import { defineStore } from "pinia";
export const useCounter = defineStore("counter", {
  state: () => ({ count: 0 }),
  actions: { inc() { this.count += 1; } },
});
