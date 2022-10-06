<script setup lang="ts">
import { formList, ModeEnum, useFvsionStore } from "../stores";
import { getAPI } from "../utils";
import ServerStatus from "./ServerStatus.vue";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";

const props = defineProps<{
  mode: string;
}>();

const isImgMode = ref(false);

// TODO, once painterro error fixed, maybe can improve this logic later
if (["img2img", "inpainting"].includes(props.mode)) {
  isImgMode.value = true;
} else {
  isImgMode.value = false;
}

// TODO, add button to reset to default, need to be careful against custom value per page, like mode etc
// use fvsionStore to help with multipage/components input
const fvsionStr = useFvsionStore();
const { fvsion } = storeToRefs(fvsionStr);

fvsion.value.mode = props.mode as ModeEnum;

// change API to unified "pipe" for t2i, i2i, inpainting (except lowvram, still buggy), fvsion(.value).mode will automatically assign the right pipe in diffusers_pipe
const api = props.mode == "lowvram" ? "lowvram" : "pipe";
const apiArt = getAPI(api);

const genArt = (): void => {
  // assign a unit uuid
  // TODO some logic like preventing resending an exact same prompt later?
  fvsion.value.uuid = uuidv4();
  // use toRaw to ensure objects send actually is the inner object, i.e. not the proxy
  let j = toRaw(fvsion.value);
  console.log(j);

  axios.post(apiArt, j).then((response: { data: any }) => {
    console.log(response.data);
  });
};

// check to display, if element is made to display in all mode or in selected mode
const isModeIn = (s: string[]) => {
  return s.includes("all") || s.includes(props.mode);
};

// when Generate Button clicked, perform genArt()
const formSubmit = (e: any) => {
  e.preventDefault();
  genArt();
};
</script>

<template>
  <div
    class="flex flex-col flex-wrap justify-between gap-2 px-2 md:flex-row w-full pt-2"
  >
    <ServerStatus></ServerStatus>
    <!-- <SavedStatus v-if="isImgMode"></SavedStatus> -->
    <span>Mode: {{ props.mode }}</span>
    <form class="w-full" @submit="formSubmit" name="aiform">
      <div class="flex flex-row w-full">
        <input
          type="text"
          placeholder="A beautiful cat"
          class="input input-bordered input-primary w-full text-black"
          id="aiprompt"
          v-model="fvsion.prompt"
        />

        <button class="btn btn-primary flex-none mx-1" type="submit">
          Generate Art
        </button>
      </div>
      <div class="form-control">
        <label class="label input-group">
          <span class="label-text">Allow NSFW</span>
          <input
            type="checkbox"
            class="checkbox checkbox-primary"
            v-model="fvsion['allowNSFW']"
        /></label>
      </div>
      <div v-for="f in formList">
        <div v-if="isModeIn(f.mode)">
          <div class="form-control">
            <label class="label input-group">
              <span class="label-text" :class="f.label_class">{{
                f.label
              }}</span>
              <input
                :type="f.type"
                :min="f.min"
                :max="f.max"
                :step="f.step"
                :class="f.class"
                v-model="fvsion[f.model]"
              />
            </label>
            <input
              type="number"
              :min="f.min"
              :max="f.max"
              :step="f.step"
              class="input input-bordered input-primary w-24 text-black"
              v-model="fvsion[f.model]"
            />
          </div>
        </div>
      </div>
    </form>

    <!-- <div class="diagnostic">
      <pre>{{ fvsion }}</pre>
    </div> -->
  </div>
</template>
