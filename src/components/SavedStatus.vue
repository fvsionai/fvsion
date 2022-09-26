<script setup lang="ts">
import { useImgPtroStore } from "../stores";
import { checkPID } from "../utils";

import { useTimeAgo } from "@vueuse/core";

const imgPtroStr = useImgPtroStore();
const { imgPtro, isImgSaved, checkMark, alertType } = storeToRefs(imgPtroStr);

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
        >Img Prompt Status: {{ checkMark }} last saved at {{ timeAgo }}. Click
        save icon on Painterro bottom right before generating your img2img.
      </span>
    </div>
  </div>
</template>
