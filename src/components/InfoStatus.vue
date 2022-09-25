<script setup lang="ts">
import { useServerStore } from "../stores";
import { checkPID } from "../utils";
import { DateTime, Duration } from "luxon";

const serverStr = useServerStore();
const { isServerRunning, checkMark, alertType } = storeToRefs(serverStr);

const timeLastCheck = useStorage("timeLastCheck", DateTime.now());

// continously check server status when it is offline, in case server delay start
// if (!isServerRunning.value) {
//   setInterval(checkPID, 5000);
// }

const updateServerStatus = (e: any) => {
  checkPID();
  timeLastCheck.value = DateTime.now();
};
</script>

<template>
  <div class="alert p-1 my-2 text-xs" :class="alertType">
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
      <span
        >API Server status: {{ checkMark }} last checked at {{ timeLastCheck }}
      </span>
      <button class="bg-zinc-400 rounded" @click="updateServerStatus">
        Update
      </button>
    </div>
  </div>
</template>
