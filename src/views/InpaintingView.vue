<script setup lang="ts">
import InpaintingInput from "@/components/InpaintingInput.vue";
</script>

<template>
  <div class="grid md:grid-cols-2 grid-cols-1">
    <div class="col-span-1">
      <SdForm mode="img2img"></SdForm>
    </div>

    <div class="col-span-1">
      <InpaintingInput mode="img2img"></InpaintingInput>
    </div>
  </div>
</template>
