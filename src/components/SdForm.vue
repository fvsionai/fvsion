<script setup lang="ts">
import { defaultFvsionModel, serverStore } from "../stores";
import { getAPI } from "../utils";
import InfoStatus from "./InfoStatus.vue";
const axios: any = inject("axios"); // inject axios

let serverStr = storeToRefs(serverStore());

// to be made from props, i.e. based on parent view
const apiArt = getAPI("txt2img");

const aiInput = ref(defaultFvsionModel);

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

const genArt = (): void => {
  let j = aiInput.value;
  axios.post(apiArt, j).then((response: { data: any }) => {
    console.log(j);
    console.log(response);
    console.log(response.data);
  });
};

const formSubmit = (e: any) => {
  e.preventDefault();
  checkPID();
  genArt();
};
</script>

<template>
  <div
    class="flex flex-col flex-wrap justify-between gap-2 px-2 md:flex-row w-full pt-2"
  >
    <form class="w-full" @submit="formSubmit" name="aiform">
      <div class="flex flex-row w-full">
        <input
          type="text"
          placeholder="A beautiful cat"
          class="input input-bordered input-primary w-full"
          id="aiprompt"
          v-model="aiInput.prompt"
        />

        <button class="btn btn-primary flex-none mx-1" type="submit">
          Generate Art
        </button>
      </div>

      <div>
        <InfoStatus
          :is-server-running="serverStr.isServerRunning.value"
        ></InfoStatus>
        <JobStatus></JobStatus>
      </div>
      <div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Height </span>
            <input
              type="range"
              min="8"
              max="1024"
              step="8"
              class="range range-primary"
              v-model="aiInput.height"
          /></label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Width </span>
            <input
              type="range"
              min="8"
              max="1024"
              step="8"
              class="range range-primary"
              v-model="aiInput.width"
          /></label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Number of Inference Steps </span>
            <input
              type="range"
              min="1"
              max="100"
              class="range range-primary"
              v-model="aiInput.num_inference_steps"
          /></label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Guidance Scale </span>
            <input
              type="range"
              min="0"
              max="30"
              step="0.1"
              class="range range-primary"
              v-model="aiInput.guidance_scale"
          /></label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Eta </span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              class="range range-primary"
              v-model="aiInput.eta"
          /></label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Seed </span>
            <input
              type="range"
              min="0"
              max="9999"
              class="range range-primary"
              v-model="aiInput.seed"
          /></label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">Allow NSFW? </span>
            <input
              type="checkbox"
              class="checkbox checkbox-primary"
              v-model="aiInput.allowNSFW"
          /></label>
        </div>
      </div>
    </form>

    <div>
      <pre> {{ aiInput }}</pre>
    </div>
  </div>
</template>
