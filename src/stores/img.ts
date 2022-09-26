export interface imgPtro {
  image: string;
  draw_image?: {
    name: string;
    path: string;
    type: string;
  };
}

export const useImgPtroStore = defineStore("imgPtroStore", {
  state: () => ({
    imgPtro: ref("blank"),
    isImgSaved: ref(false),
    checkMark: ref("Not saved yet."),
    alertType: ref("alert-error"),
  }),
  actions: {
    set(imgPtro: string, isImgSaved: boolean) {
      this.imgPtro = imgPtro;
      this.isImgSaved = true;
      if (isImgSaved) {
        this.checkMark = "Saved.";
        this.alertType = "alert-info";
      } else {
        this.checkMark = "Not saved yet.";
        this.alertType = "alert-error";
      }
    },
    reset() {
      this.imgPtro = "blank";
      this.isImgSaved = false;
      this.checkMark = "Not saved yet.";
      this.alertType = "alert-error";
    },
  },
});
