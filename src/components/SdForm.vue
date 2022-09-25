<script setup lang="ts">
import { defaultFvsionModel } from "../stores";
import { getAPI } from "../utils";
import InfoStatus from "./InfoStatus.vue";
import { v4 as uuidv4 } from "uuid";

const axios: any = inject("axios"); // inject axios

// to be made from props, i.e. based on parent view
const apiArt = getAPI("txt2img");

// TODO, maybe insert useStorage, either here on in the store to save default for subsequent sessions
// then add button to reset to default
const aiInput = ref(defaultFvsionModel);

const genArt = (): void => {
  aiInput.value.uuid = uuidv4();
  let j = aiInput.value;

  axios.post(apiArt, j).then((response: { data: any }) => {
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
    <InfoStatus></InfoStatus>

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
