<script setup lang="ts">
import ImgInput from "@/components/ImgInput.vue";
</script>

<template>
  <div class="grid md:grid-cols-2 grid-cols-1 mx-8">
    <div class="col-span-1">
      <SdForm mode="img2img"></SdForm>
    </div>

    <div class="col-span-1">
      <ImgInput mode="img2img"></ImgInput>
    </div>
  </div>
</template>
