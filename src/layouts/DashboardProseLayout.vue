<script lang="ts" setup>
import { topNavStore } from "@/stores/app";
import { breakpointsTailwind } from "@vueuse/core";

/* after navigation on small screens, close the nav drawer */
const breakpoints = useBreakpoints(breakpointsTailwind);
const lgAndLarger = breakpoints.greater("lg");
const open = ref(false);
const route = useRoute();

const { isNavAppear } = storeToRefs(topNavStore());

watch(route, () => {
  if (!lgAndLarger.value) open.value = false;
});

onMounted(() => {
  if (lgAndLarger.value) open.value = true;

  var prev = window.pageYOffset;
  window.addEventListener("scroll", () => {
    var current = window.pageYOffset;
    if (prev > current) {
      // when prev is less than current, means scrolling up, thus show AppTopBar
      isNavAppear.value = true;
    } else {
      // when prev is more than current, means scrolling down, thus hide AppTopBar
      isNavAppear.value = false;
    }
    if (current === 0) {
      // when at the top, maybe do something special?, for now none
    }
    prev = current;
  });
});
</script>

<template>
  <div class="flex height-control w-full max-w-full transition-colors">
    <NavDrawer v-model="open" />
    <div
      class="flex max-w-full flex-grow flex-col bg-zinc-100 text-zinc-900 transition-all dark:bg-zinc-900 dark:text-zinc-100"
      :class="{ 'lg:pl-64': open }"
    >
      <AppTopBar v-model="open" />
      <div
        class="prose mx-auto grow px-2 pb-2 pt-14 text-black dark:prose-invert dark:text-white md:prose-xl md:w-screen"
      >
        <main>
          <router-view />
        </main>
      </div>
      <AppFooter />
    </div>
  </div>
</template>
