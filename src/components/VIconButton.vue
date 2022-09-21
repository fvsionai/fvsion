<template>
  <component :is="component" v-wave class="rounded-full focus:outline-none focus-visible:ring focus-visible:ring-primary p-1">
    <slot />
  </component>
</template>

<script lang="ts" setup>
import { Ref } from "vue";

withDefaults(
  defineProps<{
    component?: string;
  }>(),
  {
    component: "button",
  }
);
</script>
