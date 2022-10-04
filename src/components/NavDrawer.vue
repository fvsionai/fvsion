<script lang="ts" setup>
import { breakpointsTailwind } from "@vueuse/core";
import BrandLogo from "./images/BrandLogo.vue";
import BrandType from "./images/BrandType.vue";
import { propsToAttrMap } from "@vue/shared";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

/* close the nav whenever clicked outside on small screens */
const breakpoints = useBreakpoints(breakpointsTailwind);
const lgAndLarger = breakpoints.greater("lg");
const navContainer = ref(null);
onClickOutside(navContainer, () => {
  if (!lgAndLarger.value) emit("update:modelValue", false);
});

/* main navigation links for side drawer */
const navLinks = [
  {
    text: "Home",
    to: "/",
    icon: "ic:baseline-home",
  },
  {
    text: "Img2Img",
    to: "/img2img",
    icon: "ic:baseline-home",
  },
  {
    text: "Inpainting",
    to: "/inpainting",
    icon: "ic:baseline-home",
  },
  {
    text: "lowVRAM",
    to: "/lowvram",
    icon: "ic:baseline-home",
  },
];

const navLinksSecond = [
  // {
  //   text: "Privacy",
  //   to: "/privacy",
  //   icon: "ic:baseline-privacy-tip",
  // },
  // {
  //   text: "ToS",
  //   to: "/terms",
  //   icon: "ic:baseline-info",
  // },
  {
    text: "Support",
    to: "/support",
    icon: "bi:people-fill",
  },
  {
    text: "About",
    to: "/about",
    icon: "ic:baseline-info",
  },
];

const isDark = useDark();
const toggleDark = () => {
  // if small screen, close drawer
  if (!lgAndLarger.value) {
    emit("update:modelValue", false);
  }
  useToggle(isDark)();
};
</script>

<template>
  <!-- background blur on smaller screens -->
  <transition enter-from-class="opacity-0" leave-to-class="opacity-0">
    <div
      class="fixed z-40 h-full w-full bg-black bg-opacity-50 backdrop-blur-sm backdrop-filter transition-opacity lg:hidden"
      v-if="modelValue"
    ></div>
  </transition>

  <!-- nav drawer -->
  <transition
    enter-from-class="-translate-x-full"
    leave-to-class="-translate-x-full"
  >
    <div
      v-if="modelValue"
      ref="navContainer"
      class="nav-container fixed z-50 flex h-full max-h-full w-64 flex-col justify-between divide-y overflow-y-auto bg-zinc-500 bg-cover py-1 px-2 text-zinc-100 shadow-lg transition-transform dark:shadow-none"
    >
      <nav class="py-2">
        <span class="nav-button">
          <brand-type></brand-type>
        </span>
      </nav>

      <nav class="flex flex-shrink-0 flex-grow flex-col space-y-2 py-2">
        <div class="nav-button" @click="toggleDark()">
          <span
            class="iconify mr-2 h-5 w-5 dark:hidden"
            data-icon="akar-icons:sun-fill"
          >
          </span>
          <span class="dark:hidden"> Theme: Light </span>
          <span
            class="iconify mr-2 hidden h-5 w-5 dark:block"
            data-icon="akar-icons:moon-fill"
          ></span>
          <span class="hidden dark:block"> Theme: Dark </span>
        </div>
        <router-link
          v-for="{ text, to, icon } in navLinks"
          v-wave
          class="nav-button"
          exact-active-class="primary text-zinc-100"
          :to="to"
        >
          <span class="iconify mr-2 h-5 w-5" :data-icon="icon"></span>
          <span>{{ text }}</span>
        </router-link>
      </nav>

      <nav class="py-2">
        <router-link
          v-for="{ text, to, icon } in navLinksSecond"
          v-wave
          class="nav-button"
          exact-active-class="primary text-zinc-100"
          :to="to"
        >
          <span class="iconify mr-2 h-5 w-5" :data-icon="icon"></span>
          <span>{{ text }}</span>
        </router-link>
      </nav>

      <!-- <nav class="py-2" v-if="user">
        <button @click="signOut" class="nav-button w-full">
          <i-carbon-logout class="mr-2 h-5 w-5" />
          Sign Out
        </button>
        <span class="nav-button w-full">{{ user.email }}</span>
      </nav>
      <nav class="py-2" v-else>
        <router-link
          v-wave
          class="nav-button"
          exact-active-class="primary text-zinc-100"
          to="/signin"
        >
          <span class="iconify mr-2 h-5 w-5" data-icon="carbon:login"></span>
          <span>Sign In</span>
        </router-link>
      </nav> -->
    </div>
  </transition>
</template>

<style scoped>
/* .nav-container {
  background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7))
    url("/img/base/pattern.png");
} */

.nav-button {
  @apply flex  items-center rounded p-2 text-sm transition-colors focus:outline-none focus:ring-1 focus:ring-primary-focus;
}
</style>
