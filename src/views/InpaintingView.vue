<script setup lang="ts">
import InpaintingInput from "@/components/InpaintingInput.vue";
</script>

<template>
  <div class="grid md:grid-cols-2 grid-cols-1">
    <div class="col-span-1">
      <SdForm mode="inpainting"></SdForm>
    </div>

    <div class="col-span-1">
      <InpaintingInput mode="inpainting"></InpaintingInput>
    </div>
  </div>
</template>
