export const pinia = createPinia();

export * from "./job";
export * from "./app";

export const isBrowser = typeof window !== "undefined";
export const isDev = process.env.NODE_ENV === "development";
export const isAcceptGTM = useStorage("isAcceptGTM", false);

export const defaultFvsionModel = {
  prompt: "a white cat with red hat",
  mode: "txt2img",
  out_image: {
    name: "string",
    type: "string",
    path: "string",
  },
  init_image: {
    name: "string",
    type: "string",
    path: "string",
  },
  mask_image_type: "default",
  mask_image: {
    name: "string",
    type: "string",
    path: "string",
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
