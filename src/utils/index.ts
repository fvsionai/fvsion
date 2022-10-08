import { useServerStore, pinia } from "../stores";

import axios from "axios";
const serverStr = useServerStore(pinia);
const { isServerRunning } = storeToRefs(serverStr);

export * from "./app.config";

export const API_library = {
  root: "http://localhost:4242/api/",
  version: "v00",
  functionList: [
    "",
    "pipe",
    "upscaler",
    "lowvram",
    "pid",
    "save-as-base64",
    "fvsionModel",
  ],
};

export function getAPI(s: string) {
  if (API_library.functionList.includes(s)) {
    return API_library.root + API_library.version + "/" + s;
  } else {
    throw new Error("API not found");
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
        isServerRunning.value = true;
        serverStr.set(true);
      } else {
        console.log("PID : " + response.data.pid + ". Server is offline");
        isServerRunning.value = false;
        serverStr.set(false);
      }
    })
    .catch(function (error: any) {
      isServerRunning.value = false;
      serverStr.set(false);
      console.log(error);
    });
}
