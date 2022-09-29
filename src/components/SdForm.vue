<script setup lang="ts">
import { defaultFvsionModel, formList } from "../stores";
import { getAPI } from "../utils";
import ServerStatus from "./ServerStatus.vue";
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


// check to display, if element is made to display in all mode or in selected mode
const isModeIn = (s: string[]) => {
  return (s.includes("all") || s.includes(props.mode))
}

// when Generate Button clicked, perform genArt()
const formSubmit = (e: any) => {
  e.preventDefault();
  genArt();
};
</script>

<template>
  <div class="flex flex-col flex-wrap justify-between gap-2 px-2 md:flex-row w-full pt-2">
    <ServerStatus></ServerStatus>
    <SavedStatus v-if="isImgMode"></SavedStatus>

    <form class="w-full" @submit="formSubmit" name="aiform">
      <div class="flex flex-row w-full">
        <input type="text" placeholder="A beautiful cat" class="input input-bordered input-primary w-full" id="aiprompt"
          v-model="aiInput.prompt" />

        <button class="btn btn-primary flex-none mx-1" type="submit">
          Generate Art
        </button>
      </div>

      <div v-for="f in formList">
        <div v-if="isModeIn(f.mode)">
          <div class="form-control">
            <label class="label input-group">
              <span class="label-text" :class="f.label_class">{{f.label}}</span>
              <input :type=f.type :min=f.min :max=f.max :step=f.step :class=f.class
                v-model="aiInput[f.model]" /></label>
          </div>
        </div>
      </div>

              
        <!-- <div class="form-control">
          <label class="label input-group">
            <span class="label-text">Init Image</span>
            <input
              type="file"
              accept="image/*"
              name="init_file"
              @change="changeImg"
          /></label>
        </div> -->
    </form>

    <div class="card card-body">
      <div class="mode-all">
        <span class="text-sm p-1">Mode : {{ aiInput.mode }}</span>
      </div>
      <div class="mode-txt2img" v-if="!isImgMode">
        <span class="text-sm p-1">Height : {{ aiInput.height }}</span>
        <span class="text-sm p-1">Width : {{ aiInput.width }}</span>
      </div>
      <div class="mode-all">
        <span class="text-sm p-1">Steps : {{ aiInput.num_inference_steps }}</span>
        <br />
        <span class="text-sm p-1">Guidance : {{ aiInput.guidance_scale }}</span>
        <span class="text-sm p-1">Eta : {{ aiInput.eta }}</span>
        <span class="text-sm p-1">Seed : {{ aiInput.seed }}</span>
        <span class="text-sm p-1">Allow NSFW : {{ aiInput.allowNSFW }}</span>
      </div>
      <div class="mode-img2img" v-if="isImgMode">
        <span class="text-sm p-1">Strength : {{ aiInput.strength }}</span>
      </div>
    </div>
    <!-- <div class="diagnostic">
      <pre>{{ aiInput }}</pre>
    </div> -->
  </div>
</template>
