export const topNavStore = defineStore("topNavStore", {
  state: () => ({
    isNavAppear: useLocalStorage("topNavStore", true),
  }),
  actions: {
    set(isNavAppear: boolean) {
      this.isNavAppear = isNavAppear;
    },
    toggle() {
      this.isNavAppear = !this.isNavAppear;
    },
  },
});
