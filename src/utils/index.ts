export * from "./app.config";

export const API_library = {
  root: "http://localhost:4242/api/",
  version: "v00",
  functionList: ["txt2img", "img2img", "inpainting", "pid"],
};

export function getAPI(s: string) {
  if (API_library.functionList.includes(s)) {
    return API_library.root + API_library.version + "/" + s;
  }
}
