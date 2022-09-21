<script lang="ts" setup>
/* modelValue here refers to whether or not to show side nav drawer */

import { topNavStore } from "@/stores/app";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const isDark = useDark();
const toggleDark = useToggle(isDark);

const toggleSideNav = function () {
  emit("update:modelValue", !props.modelValue);
};

const { isNavAppear } = storeToRefs(topNavStore());
</script>

<template>
  <transition name="slide-fade">
    <header
      class="fixed top-0 z-30 w-full bg-inherit p-3 shadow"
      ref="scrollnav"
      v-show="isNavAppear"
    >
      <div class="relative flex flex-row justify-between">
        <div class="flex">
          <v-icon-button @click="toggleSideNav()">
            <i-carbon-menu class="h-6 w-6" />
          </v-icon-button>
        </div>
        <div class="ml-auto flex">
          <v-icon-button @click="toggleDark()">
            <i-carbon-sun class="h-6 w-6 dark:hidden" />
            <i-carbon-moon class="hidden h-6 w-6 dark:block" />
          </v-icon-button>
        </div>
      </div>
    </header>
  </transition>
</template>

<style>
/*
  Enter and leave animations can use different
  durations and timing functions.
*/
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
