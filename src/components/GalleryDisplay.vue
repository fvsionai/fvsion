<script setup lang="ts">
import { Splide, SplideSlide, Options } from "@splidejs/vue-splide";
import "@splidejs/vue-splide/css";

import path from "path";
import { isDev, rootBuild } from "@/stores";

function getDir(pathToOutputs: string, filenametype: string) {
  // pathToOutputs, e.g. = "outputs/tmp"
  // filenametype, e.g. = "init.png"

  let p = "";

  if (isDev) {
    p = path.join(pathToOutputs, filenametype);
  } else {
    p = path.join(rootBuild, pathToOutputs, filenametype);
  }

  return p;
}

defineComponent({
  components: {
    Splide,
    SplideSlide,
  },
});

const main = ref<InstanceType<typeof Splide>>();
const thumbs = ref<InstanceType<typeof Splide>>();

// splide options
const mainOptions: Options = {
  type: "loop",
  perPage: 1,
  perMove: 1,
  gap: "1rem",
  pagination: false,
};
const thumbsOptions: Options = {
  type: "slide",
  rewind: true,
  gap: "1rem",
  pagination: false,
  fixedWidth: 110,
  fixedHeight: 70,
  cover: true,
  focus: "center",
  isNavigation: true,
  updateOnMove: true,
};

const slideList = [
  {
    src: getDir(
      "outputs",
      "c6f35738f6b5_retrofuturistic-sorceress-plat_upscaled.webp"
    ),
    alt: "Sample 1",
    id: "slide_01",
  },
  { src: "/android-chrome-512x512.png", alt: "Sample 2", id: "slide_02" },
  { src: "/android-chrome-512x512.png", alt: "Sample 2", id: "slide_03" },
  { src: "/android-chrome-512x512.png", alt: "Sample 2", id: "slide_04" },
  { src: "/android-chrome-512x512.png", alt: "Sample 2", id: "slide_05" },
];

onMounted(() => {
  const thumbsSplide = thumbs.value?.splide;
  const test = main.value?.splide;
  if (thumbsSplide) {
    main.value?.sync(thumbsSplide);
  }
});
</script>

<template>
  <Splide :options="mainOptions" aria-label="My Favorite Images" ref="main">
    <SplideSlide v-for="slide in slideList" :key="slide.id">
      <img :src="slide.src" :alt="slide.alt" />
    </SplideSlide>
  </Splide>
  <Splide
    :options="thumbsOptions"
    aria-label="The carousel with thumbnails. Selecting a thumbnail will change the main carousel"
    ref="thumbs"
  >
    <SplideSlide v-for="slide in slideList" :key="slide.id">
      <img :src="slide.src" :alt="slide.alt" />
    </SplideSlide>
  </Splide>
</template>
