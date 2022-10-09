<script setup lang="ts">
import { Splide, SplideSlide } from "@splidejs/vue-splide";
import "@splidejs/vue-splide/css";

defineComponent({
  components: {
    Splide,
    SplideSlide,
  },
});

// splide options
const splideOptions = {
  rewind: true,
  gap: "1rem",
  perPage: 2,
};

const slideList = [
  { src: "/android-chrome-192x192.png", alt: "Sample 1", id: "slide_01" },
  { src: "/android-chrome-512x512.png", alt: "Sample 2", id: "slide_02" },
  { src: "/android-chrome-512x512.png", alt: "Sample 2", id: "slide_03" },
];
</script>

<template>
  <Splide :options="splideOptions" aria-label="My Favorite Images">
    <SplideSlide v-for="slide in slideList" :key="slide.id">
      <img :src="slide.src" :alt="slide.alt" />
      <!-- <img src="/android-chrome-192x192.png" alt="Sample 1" /> -->
    </SplideSlide>
  </Splide>
</template>
