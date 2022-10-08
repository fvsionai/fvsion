<script setup lang="ts">
import { ModeEnum, useFvsionStore } from "../stores";

const props = defineProps<{
  mode: string;
}>();

// use fvsionStore to help with multipage/components input
const fvsionStr = useFvsionStore();
const { fvsion } = storeToRefs(fvsionStr);

fvsion.value.mode = props.mode as ModeEnum;
</script>

<template>
  <div
    class="flex flex-col flex-wrap justify-between gap-2 px-2 md:flex-row w-full pt-2"
  ></div>
</template>
