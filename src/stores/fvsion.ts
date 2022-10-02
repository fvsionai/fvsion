import { FvsionModel } from "./schema";

export const defaultFvsionModel: FvsionModel = {
  prompt: "a white cat with red hat",
  uuid: "default",
  mode: "txt2img",
  out_image: {
    name: "string",
    type: "string",
    path: "string",
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
  num_inference_steps: 16,
  guidance_scale: 7.5,
  eta: 0,
  strength: 0.85,
  seed: 1024,
  allowNSFW: false,
  doJSON: true,
};

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
    min: 8,
    max: 1024,
    step: 8,
    mode: ["txt2img"],
    model: "height",
    label: "Height",
    label_class: "",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 8,
    max: 1024,
    step: 8,
    mode: ["txt2img"],
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
    max: 9999,
    step: 1,
    mode: ["all"],
    model: "seed",
    label: "Seed",
    label_class: "",
  },
  {
    type: "checkbox",
    class: "checkbox checkbox-primary",
    min: 8,
    max: 1024,
    step: 8,
    mode: ["all"],
    model: "allowNSFW",
    label: "Allow NSFW",
    label_class: "",
  },
  {
    type: "range",
    class: "range range-primary",
    min: 0,
    max: 1,
    step: 0.01,
    mode: ["img2img"],
    model: "strength",
    label: "Strength",
    label_class: "",
  },
];
