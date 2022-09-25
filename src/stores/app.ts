export const topNavStore = defineStore("topNavStore", {
  state: () => ({
    isNavAppear: useStorage("topNavStore", true),
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

export const useServerStore = defineStore("server", {
  state: () => ({
    isServerRunning: ref(false),
    checkMark: ref("Offline"),
    alertType: ref("alert-error"),
  }),
  actions: {
    set(isServerRunning: boolean) {
      this.isServerRunning = isServerRunning;
      if (isServerRunning) {
        this.checkMark = "Online";
        this.alertType = "alert-info";
      } else {
        this.checkMark = "Offline";
        this.alertType = "alert-error";
      }
    },
  },
});
