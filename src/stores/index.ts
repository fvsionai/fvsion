export const pinia = createPinia();

export * from "./job";
export * from "./app";
export * from "./img";
export * from "./fvsion";
export type { ModeEnum, FileModel } from "./schema";

export const isBrowser = typeof window !== "undefined";
export const isDev = process.env.NODE_ENV === "development";
export const isAcceptGTM = useStorage("isAcceptGTM", false);
