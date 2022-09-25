<script setup lang="ts">
import PainterroContainerVue from "@/components/PainterroContainer.vue";
</script>

<template>
  <div class="grid md:grid-cols-2 grid-cols-1">
    <div class="col-span-1">
      <SdForm></SdForm>
    </div>

    <div class="col-span-1">
      <PainterroContainerVue></PainterroContainerVue>
    </div>
  </div>
</template>
