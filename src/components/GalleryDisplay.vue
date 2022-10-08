<script setup lang="ts">
import { Splide, SplideSlide, Options } from "@splidejs/vue-splide";
import "@splidejs/vue-splide/css";

import { isDev, root } from "@/stores";
import path from "path";
import fs from "fs/promises";

function getDir(pathToOutputs: string, filenametype: string) {
  // pathToOutputs, e.g. = "outputs/tmp"
  // filenametype, e.g. = "init.png"
  let p = "";

  // slightly different way to load if on Dev vs on Production/Build
  if (isDev) {
    // p = path.join(pathToOutputs, filenametype);
    p = pathToOutputs + "/" + filenametype;
  } else {
    p = path.join(root, pathToOutputs, filenametype);
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
  height: 720,
  breakpoints: {
    600: {
      height: 360,
    },
  },
};

const thumbsOptions: Options = {
  type: "slide",
  rewind: true,
  gap: "1rem",
  pagination: false,
  fixedWidth: 100,
  fixedHeight: 60,
  cover: true,
  focus: "center",
  isNavigation: true,
  updateOnMove: true,
  breakpoints: {
    600: {
      fixedWidth: 60,
      fixedHeight: 44,
    },
  },
};

interface slideObj {
  src: string;
  alt: string;
  id: string;
}

// const imgList: slideObj[] = [];
let dummy: slideObj[] = [];
const imgList = useStorage("imgList", dummy);

onMounted(async () => {
  const thumbsSplide = thumbs.value?.splide;
  if (thumbsSplide) {
    main.value?.sync(thumbsSplide);
  }

  try {
    // TODO, maybe have a more detailed read into subfolder?
    const files: string[] = await fs.readdir(path.join(root, "outputs"));

    const dummyList: slideObj[] = [];
    files.forEach((el, idx) => {
      // get file extension, e.g. "png"
      const ext = path.extname(el).slice(1);

      // if image check via file ext/type, remember that "type" is reserved word in JS
      if (["webp", "png", "jpg", "jpeg", "gif", "bmp"].includes(ext)) {
        let s: slideObj = {
          src: getDir("outputs", el),
          alt: el,
          id: idx + "_img",
        };
        dummyList.push(s);
      }
    });

    // replace the imgList in useStorage with newly read file via readdir
    imgList.value = dummyList;
    // console.log(imgList.value); // for diagnostic
  } catch (err) {
    console.error(err);
  }
});
</script>

<template>
  <Splide
    :options="mainOptions"
    aria-label="Main display, showing generated images from outputs folder"
    ref="main"
    id="splide_main"
  >
    <SplideSlide v-for="slide in imgList" :key="slide.id">
      <img :src="slide.src" :alt="slide.alt" />
    </SplideSlide>
  </Splide>
  <Splide
    :options="thumbsOptions"
    aria-label="The carousel with thumbnails. Selecting a thumbnail will change the main carousel"
    ref="thumbs"
  >
    <SplideSlide v-for="slide in imgList" :key="slide.id" id="splide_thumbnail">
      <img :src="slide.src" :alt="slide.alt" />
    </SplideSlide>
  </Splide>
</template>

<style>
#splide_main .splide__slide img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

#splide_thumbnail .splide__slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.splide__slide {
  opacity: 0.6;
}

.splide__slide.is-active {
  opacity: 1;
}

.splide__track--nav > .splide__list > .splide__slide.is-active {
  /* border-color: white; */
  @apply border-primary;
}
</style>
