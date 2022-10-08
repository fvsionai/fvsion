import { FvsionModel } from "./schema";

export const defaultFvsionModel: FvsionModel = {
  prompt: "A fantasy landscape, trending on artstation",
  uuid: "default",
  mode: "txt2img",
  out_image: {
    name: "init",
    type: "png",
    path: "outputs",
  },
  init_image: {
    name: "init",
    type: "png",
    path: "outputs/tmp",
  },
  mask_image_type: "default",
  mask_image: {
    name: "mask",
    type: "png",
    path: "outputs/tmp",
  },
  mask_color: "white",
  height: 512,
  width: 512,
  num_inference_steps: 30,
  guidance_scale: 6.5,
  eta: 0,
  strength: 0.85,
  seed: 1024,
  allowNSFW: false,
  doJSON: true,
  upscaler: {
    bg: "realesrgan",
    bg_version: "RealESRGAN_x4plus",
    face: "gfpgan",
    face_version: "GFPGANv1.4",
    factor: 2,
    suffix: "upscaled",
    only_center_face: false,
    has_aligned: false,
    weight: 0.5,
    type: "auto",
  },
};

export const useFvsionStore = defineStore("fvsion", {
  state: () => ({
    fvsion: useStorage("fvsion", defaultFvsionModel),
  }),
  actions: {
    set(f: FvsionModel) {
      this.fvsion = f;
    },
  },
});

interface FormInput {
  [index: string]: string | string[] | number;
  type: string;
  class: string;
  min: number;
  max: number;
  step: number;
  mode: string[];
  model: string;
  label: string;
  label_class: string;
}

export const formList: FormInput[] = [
  {
    type: "range",
    class: "range range-primary",
    min: 64,
    max: 2048,
    step: 64,
    mode: ["txt2img", "lowvram"],
    model: "height",
    label: "Height",
    label_class: "",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 64,
    max: 2048,
    step: 64,
    mode: ["txt2img", "lowvram"],
    model: "width",
    label: "Width",
    label_class: "",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 1,
    max: 100,
    step: 1,
    mode: ["all"],
    model: "num_inference_steps",
    label: "Inference Steps",
    label_class: "w-40",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 0,
    max: 30,
    step: 0.1,
    mode: ["all"],
    model: "guidance_scale",
    label: "Guidance Scale",
    label_class: "w-40",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 0,
    max: 1,
    step: 0.1,
    mode: ["all"],
    model: "eta",
    label: "Eta",
    label_class: "",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 0,
    max: 9999999999,
    step: 1,
    mode: ["all"],
    model: "seed",
    label: "Seed",
    label_class: "",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 0,
    max: 1,
    step: 0.01,
    mode: ["img2img", "inpainting"],
    model: "strength",
    label: "Strength",
    label_class: "",
  },
];
