import path from "path";

export const pinia = createPinia();

export * from "./job";
export * from "./app";
export * from "./img";
export * from "./fvsion";
export type { ModeEnum, FileModel, Upscaler, UpscalerModel } from "./schema";

export const isBrowser = typeof window !== "undefined";
export const isDev = process.env.NODE_ENV === "development";
export const isAcceptGTM = useStorage("isAcceptGTM", false);

// going updir from /fvsion/release/0.0.1/win-unpacked/resources/app.asar/dist
// to /fvsion
const relative = isDev ? ".." : "../../../../..";
export const root = path.join(process.env.DIST as string, relative);
