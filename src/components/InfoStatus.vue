<script setup lang="ts">
import { serverStore } from "../stores";
import { getAPI } from "../utils";

const axios: any = inject("axios"); // inject axios

let serverStr = storeToRefs(serverStore());
const isRunning = serverStr.isServerRunning.value;
// TODO, to make YES/NO to Icon
const checkMark = isRunning ? "Online" : "Offline";

const checkPID = (): void => {
  axios.get(getAPI("pid")).then((response: { data: any }) => {
    // TODO
    // if return PID data, then server is running, else offline
    if (Number(response.data.pid)) {
      serverStr.isServerRunning.value = true;
    } else {
      serverStr.isServerRunning.value = false;
    }
    console.log(response.data.pid);
  });
};

const delay = (sec: number) =>
  new Promise((res) => setTimeout(res, sec * 1000));

function retry(maxRetry: number) {
  // TODO, do I really need this JSON part to copy value and not reference?
  const maxRetry_ = JSON.parse(JSON.stringify(maxRetry));
  let expectations = true;

  if (maxRetry >= 0 && expectations) {
    async () => {
      // set the timeout to be longer for each failed start linearly
      let delaySecond = maxRetry_ - maxRetry;
      console.log(delaySecond);

      console.log(
        "Server offline, waiting for " + delaySecond + " seconds to retry."
      );
      await delay(delaySecond);
      checkPID();
      // retry until maxRetry ran out (becomes zero or server is online)
      expectations != serverStr.isServerRunning.value;
      // reduce count
      maxRetry -= 1;
    };
  } else {
    console.log("exceed maximum retry count");
  }
}

retry(20);
</script>

<template>
  <div class="alert alert-info p-1 my-2">
    <div>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="stroke-current flex-shrink-0 w-6 h-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        ></path>
      </svg>
      <span class="text-xs">API Server status: {{ checkMark }}</span>
    </div>
  </div>
</template>
