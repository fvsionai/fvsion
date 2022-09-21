export const pinia = createPinia();

export const isBrowser = typeof window !== "undefined";
export const isDev = process.env.NODE_ENV === "development";
export const isAcceptGTM = useStorage("isAcceptGTM", false);
