<script setup lang="ts">
import path from "path";
import { FileModel, ModeEnum, useFvsionStore } from "../stores";

const props = defineProps<{
  mode: string;
}>();

// use fvsionStore to help with multipage/components input
const fvsionStr = useFvsionStore();
const { fvsion } = storeToRefs(fvsionStr);

fvsion.value.mode = props.mode as ModeEnum;

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
</script>

<template>
  <div class="pt-2">
    <div>
      <span>Image and Mask Input</span>
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
    <div class="form-control">
      <label for="mask_image" class="label input-group justify-start">
        <span class="label-text w-32">Choose Mask</span>
        <input
          type="file"
          id="mask_image"
          accept="image/*"
          class="hidden"
          @change="onc_image('mask_image')"
        />
        <span class="text-sm truncate text-left ml-1 text-black">{{
          fvsion.mask_image?.name
        }}</span>
      </label>
    </div>
    <!-- <div>
      <div class="border-t-4 border-slate-300"></div>
      <div class="form-control">
        <label class="label cursor-pointer input-group">
          <span class="label-text">Mask Default (use separate mask file)</span>
          <input
            type="radio"
            name="radio-mode"
            class="radio checked:bg-primary"
            value="default"
            v-model="fvsion.mask_image_type"
          />
        </label>
      </div>
      <div class="form-control">
        <label class="label cursor-pointer input-group">
          <span class="label-text">Mask Use Alpha</span>
          <input
            type="radio"
            name="radio-mode"
            class="radio checked:bg-primary"
            value="alpha"
            v-model="fvsion.mask_image_type"
          />
        </label>
      </div>
      <div class="form-control">
        <label class="label cursor-pointer input-group">
          <span class="label-text">Mask Use White</span>
          <input
            type="radio"
            name="radio-mode"
            class="radio checked:bg-primary"
            value="white"
            v-model="fvsion.mask_image_type"
          />
        </label>
      </div>
      <span>{{ fvsion.mask_image_type }}</span>
    </div> -->
  </div>
</template>
