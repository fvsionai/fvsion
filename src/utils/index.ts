import { serverStore } from "../stores";

import axios from "axios";
const serverStr = storeToRefs(serverStore());

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

export function checkPID() {
  axios
    .get(getAPI("pid")!)
    .then((response: { data: any }) => {
      // TODO
      // if return PID data, then server is running, else offline
      if (response.data.pid) {
        console.log("PID : " + response.data.pid + ". Server is online");
        serverStr.isServerRunning.value = true;
      } else {
        console.log("PID : " + response.data.pid + ". Server is offline");
        serverStr.isServerRunning.value = false;
      }
    })
    .catch(function (error: any) {
      serverStr.isServerRunning.value = false;
      console.log(error);
    });
}
