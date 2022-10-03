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
      type: type,
    };

    fvsion.value[s] = fmodel;
  }
};
</script>

<template>
  <div>
    <form>
      <div class="form-control">
        <label for="mask_image" class="label input-group">
          <span class="label-text w-32">Choose Input</span>
          <input
            type="file"
            id="init_image"
            accept="image/*"
            class="hidden"
            @change="onc_image('init_image')"
          />
          <span class="text-sm truncate">{{ fvsion.init_image?.name }}</span>
        </label>
      </div>
      <div class="form-control">
        <label for="mask_image" class="label input-group">
          <span class="label-text w-32">Choose Mask</span>
          <input
            type="file"
            id="mask_image"
            accept="image/*"
            class="hidden"
            @change="onc_image('mask_image')"
          />
          <span class="text-sm truncate">{{ fvsion.mask_image?.name }}</span>
        </label>
      </div>
    </form>
  </div>
</template>
