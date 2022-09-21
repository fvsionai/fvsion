<script setup lang="ts">
const axios: any = inject("axios"); // inject axios

let showNotice = ref(false);
let showError = ref(false);
let showSuccess = ref(false);

axios.interceptors.request.use(
  function (config: any) {
    // Do something before request is sent
    console.log("Start Ajax Call");
    showNotice.value = true;
    return config;
  },
  function (error: any) {
    // Do something with request error
    console.log("Error");
    showError.value = true;
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  function (response: any) {
    // Do something with response data
    console.log("Done with Ajax call");
    showSuccess.value = true;
    return response;
  },
  function (error: any) {
    // Do something with response error
    console.log("Error fetching the data");
    return Promise.reject(error);
    showError.value = true;
  }
);

// interface ref <{
//     prompt: string;
//     height: number;
//     width: number;
//     num_inference_steps: number;
//     guidance_scale: number;
//     eta: number;
//     seed: number;
//     allowNSFW: boolean;
// }>

const api = "http://localhost:4242/pid";
const apiArt = "http://localhost:4242/api/v00/txt2img/";

const aiInput = ref({
  prompt: "A beautiful cat",
  height: 512,
  width: 512,
  num_inference_steps: 16,
  guidance_scale: 7.5,
  eta: 0,
  seed: 4242,
  allowNSFW: false,
});

const getList = (): void => {
  axios.get(api).then((response: { data: any }) => {
    console.log(response.data);
  });
};

let state = reactive({
  jsonInput: {},
});

const genArt = (j: any): void => {
  axios.post(apiArt, j).then((response: { data: any }) => {
    console.log(j);
    console.log(response.data);
  });
};

const formSubmit = (e: any) => {
  e.preventDefault();
  genArt(aiInput.value);
  showNotice.value = true;
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
        <span v-if="showNotice"> Prompt sent for generation. </span>
        <span v-if="showError">
          Error in sending data to python. Please wait at the start for a few
          minutes. Check if
          <a href="http://localhost:4242/docs" target="_blank" class="primary"
            >http://localhost:4242/docs</a
          >
          is live.
        </span>
        <span v-if="showSuccess">
          Prompt successfully generated. Go to `output` folder
        </span>
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
