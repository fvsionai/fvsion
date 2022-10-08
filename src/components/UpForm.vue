<script setup lang="ts">
import { FileModel, ModeEnum, useFvsionStore, UpscalerModel } from "../stores";
import { getAPI } from "../utils";
import ServerStatus from "./ServerStatus.vue";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";
import path from "path";

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

// api limit to only upscaler for UpForm
const apiImage = getAPI("upscaler");

const genImage = (): void => {
  // assign a unit uuid
  // TODO some logic like preventing resending an exact same prompt later?
  fvsion.value.uuid = uuidv4();
  fvsion.value.upscaler = toRaw(upscaler.value) as UpscalerModel;

  // use toRaw to ensure objects send actually is the inner object, i.e. not the proxy
  let j = toRaw(fvsion.value);
  console.log(j);

  axios.post(apiImage, j).then((response: { data: any }) => {
    console.log(response.data);
  });
};

// check to display, if element is made to display in all mode or in selected mode
const isModeIn = (s: string[]) => {
  return s.includes("all") || s.includes(props.mode);
};

const upscale_default = ref({
  bg: "realesrgan",
  bg_version: "RealESRGAN_x4plus",
  face: "gfpgan",
  face_version: "GFPGANv1.4",
  factor: 2,
  suffix: "upscaled",
  only_center_face: false,
  has_aligned: false,
  weight: 0.5,
  type: "auto",
});
const upscaler = useStorage("upscaler", upscale_default);

// update upscaler values
const onc_upscaler = (s: string) => {
  // e.g. factor --> upscaler_factor as id
  const params = document.getElementById("upscaler_" + s) as HTMLInputElement;

  // if upscaler params found, update it
  if (params) {
    // get the default/current upscalermodel from store/refs
    const umodel = fvsion.value.upscaler as UpscalerModel;

    if (params.type == "range" || params.type == "number") {
      // if range or number, then change to number
      umodel[s] = Number(params.value);
    } else {
      // else take as is, i.e. string
      umodel[s] = params.value;
    }

    // overwrite the latest parameters from input
    fvsion.value["upscaler"] = umodel;
  }
};

const onc_image = (s: string) => {
  const img = document.getElementById(s) as HTMLInputElement;
  if (img && img.files && img.files.length >= 1) {
    // if image exist, update the paths
    const fpname = img.files[0].path; // full file path and name and extension
    const fpath = path.dirname(fpname); // the path only
    const name = path.basename(fpname, path.extname(fpname)); // the filename only
    const type = path.extname(fpname).replace(".", ""); // the extension only (e.g. png/webp)

    const fmodel: FileModel = {
      name: name,
      path: fpath,
      type: type as FileModel["type"],
    };

    fvsion.value[s] = fmodel;
  }
};

// when Generate Button clicked, perform genImage()
const formSubmit = (e: any) => {
  e.preventDefault();
  genImage();
};
</script>

<template>
  <div
    class="flex flex-col flex-wrap justify-between gap-2 px-2 md:flex-row w-full pt-2"
  >
    <ServerStatus></ServerStatus>
    <!-- <SavedStatus v-if="isImgMode"></SavedStatus> -->
    <span>Mode: {{ props.mode }}</span>
    <form class="w-full" @submit="formSubmit" name="upscaleform">
      <div class="flex flex-row w-full justify-between">
        <div>
          <div>
            <span>Image Input</span>
          </div>
          <div class="form-control">
            <label for="init_image" class="label input-group justify-start">
              <span class="label-text w-32">Choose Input</span>
              <input
                type="file"
                id="init_image"
                accept="image/*"
                class="hidden"
                @change="onc_image('init_image')"
              />
              <span class="text-sm truncate text-left ml-1 text-black">{{
                fvsion.init_image?.name
              }}</span>
            </label>
          </div>
        </div>
        <button class="btn btn-primary flex-none mx-1" type="submit">
          Upscale Image
        </button>
      </div>
      <div>
        <input
          type="range"
          class="range range-primary"
          min="2"
          max="8"
          step="1"
          id="upscaler_factor"
          v-model="upscaler.factor"
        />
        <input
          type="number"
          class="input input-primary"
          min="2"
          max="8"
          step="1"
          id="upscaler_factor"
          v-model="upscaler.factor"
        />
      </div>
      <div class="form-control w-full max-w-xs">
        <label class="label">
          <span class="label-text"
            >Pick Upscaler Options {{ upscaler.bg_version }}</span
          >
        </label>
        <select
          id="upscaler_bg_version"
          class="select select-primary max-w-xs"
          v-model="upscaler.bg_version"
        >
          <option>RealESRGAN_x2plus</option>
          <option>RealESRGAN_x4plus</option>
          <option>RealESRGAN_x4plus_anime_6B</option>
        </select>
      </div>
      <div class="form-control w-full max-w-xs">
        <label class="label">
          <span class="label-text">Pick Face Restoration Options</span>
        </label>
        <select
          id="upscaler_face_version"
          class="select select-primary max-w-xs"
          v-model="upscaler.face_version"
        >
          <option>GFPGANv1.4</option>
          <option>RestoreFormer</option>
        </select>
      </div>
    </form>
  </div>
</template>
