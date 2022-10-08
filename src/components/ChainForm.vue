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

// use fvsionStore to help with multipage/components input
const fvsionStr = useFvsionStore();
const { fvsion } = storeToRefs(fvsionStr);

fvsion.value.mode = props.mode as ModeEnum;

const apiImage = getAPI("chain");
</script>

<template>
  <div
    class="flex flex-col flex-wrap justify-between gap-2 px-2 md:flex-row w-full pt-2"
  >
    <ServerStatus></ServerStatus>
  </div>
</template>
