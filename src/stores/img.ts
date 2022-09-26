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
    imgPtro: "blank",
    isImgSaved: false,
  }),
  actions: {
    set(imgPtro: string, isImgSaved: boolean) {
      this.imgPtro = imgPtro;
      this.isImgSaved = true;
    },
    reset() {
      this.imgPtro = "blank";
      this.isImgSaved = false;
    },
  },
});
