<script setup lang="ts">
import { serverStore } from "../stores";
import { checkPID } from "../utils";

const serverStr = serverStore();
const { isServerRunning } = storeToRefs(serverStr);

// TODO, to make YES/NO to Icon
const checkMark = isServerRunning.value ? "Online" : "Offline";
const alertType = isServerRunning.value ? "alert-info" : "alert-error";

// continously check server status when it is offline, in case server delay start
if (!isServerRunning.value) {
  setInterval(checkPID, 5000);
}
</script>

<template>
  <div class="alert p-1 my-2" :class="alertType">
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
