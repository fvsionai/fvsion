<script setup lang="ts">
import { defaultFvsionModel, serverStore } from "../stores";
const axios: any = inject("axios"); // inject axios

let serverRunning = storeToRefs(serverStore());

const apiPID = "http://localhost:4242/pid";
const apiArt = "http://localhost:4242/api/v00/txt2img/";

const aiInput = ref(defaultFvsionModel);

const checkPID = (): void => {
  axios.get(apiPID).then((response: { data: any }) => {
    console.log(response.data);
    // TODO
    // serverRunning
  });
};

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
