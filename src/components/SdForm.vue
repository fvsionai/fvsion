<script setup lang="ts">
import { defaultFvsionModel } from "../stores";
import { getAPI } from "../utils";
import InfoStatus from "./InfoStatus.vue";
import { v4 as uuidv4 } from "uuid";

const axios: any = inject("axios"); // inject axios

const props = defineProps<{
  mode: string;
}>();

const isImgMode = ref(false);

if (props.mode == "txt2img") {
  isImgMode.value = false;
} else {
  isImgMode.value = true;
}

// TODO, maybe insert useStorage, either here on in the store to save default for subsequent sessions
// then add button to reset to default, need to be careful against custom value per page, like mode etc
const aiInput = ref(defaultFvsionModel);
aiInput.value.mode = props.mode;

// to be made from props, i.e. based on parent view
const apiArt = getAPI(aiInput.value.mode);

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

      <div class="mode-all">
        <div class="form-control">
          <label class="label input-group">
            <span class="label-text">Height</span>
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
          <label class="label input-group">
            <span class="label-text">Width</span>
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
          <label class="label input-group">
            <span class="label-text w-40">Inference Steps</span>
            <input
              type="range"
              min="1"
              max="100"
              class="range range-primary"
              v-model="aiInput.num_inference_steps"
          /></label>
        </div>
        <div class="form-control">
          <label class="label input-group">
            <span class="label-text w-40">Guidance Scale</span>
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
          <label class="label input-group">
            <span class="label-text">Eta</span>
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
          <label class="label input-group">
            <span class="label-text">Seed</span>
            <input
              type="range"
              min="0"
              max="9999"
              class="range range-primary"
              v-model="aiInput.seed"
          /></label>
        </div>
        <div class="form-control">
          <label class="label input-group">
            <span class="label-text">Allow NSFW?</span>
            <input
              type="checkbox"
              class="checkbox checkbox-primary"
              v-model="aiInput.allowNSFW"
          /></label>
        </div>
      </div>
      <div class="mode-img2img" v-if="isImgMode">
        <div class="form-control">
          <label class="label input-group">
            <span class="label-text">Strength</span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              class="range range-primary"
              v-model="aiInput.strength"
          /></label>
        </div>
      </div>
    </form>

    <div>
      <div class="mode-all">
        <span class="text-sm p-1">Mode : {{ aiInput.mode }}</span>
        <span class="text-sm p-1">Height : {{ aiInput.height }}</span>
        <span class="text-sm p-1">Width : {{ aiInput.width }}</span>
        <span class="text-sm p-1"
          >Steps : {{ aiInput.num_inference_steps }}</span
        >
        <span class="text-sm p-1">Guidance : {{ aiInput.guidance_scale }}</span>
        <span class="text-sm p-1">Eta : {{ aiInput.eta }}</span>
        <span class="text-sm p-1">Seed : {{ aiInput.seed }}</span>
      </div>
      <div class="mode-img2img" v-if="isImgMode">
        <span class="text-sm p-1">Strength : {{ aiInput.strength }}</span>
      </div>
    </div>
    <div class="diagnostic">
      <pre>{{ aiInput }}</pre>
    </div>
  </div>
</template>
