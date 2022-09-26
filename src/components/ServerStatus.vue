<script setup lang="ts">
import { useServerStore } from "../stores";
import { checkPID } from "../utils";

import { useTimeAgo } from "@vueuse/core";

const serverStr = useServerStore();
const { isServerRunning, checkMark, alertType } = storeToRefs(serverStr);

let stamp = ref(Date.now());
let timeAgo = useTimeAgo(stamp);

const updateServerStatus = () => {
  console.log(Date.now());
  stamp.value = Date.now();
  timeAgo = useTimeAgo(stamp);

  checkPID();
};

updateServerStatus();
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
        >API Server status: {{ checkMark }} last checked at {{ timeAgo }}
      </span>
      <button
        class="bg-primary rounded px-2 text-white"
        @click="updateServerStatus"
      >
        Check Server
      </button>
    </div>
  </div>
</template>
