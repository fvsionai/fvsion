<script setup lang="ts">
import Painterro from "painterro";
import { defaultFvsionModel, ModeEnum, useImgPtroStore } from "../stores";
import { getAPI } from "../utils";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";

const imgPtroStr = useImgPtroStore();
const { imgPtro } = storeToRefs(imgPtroStr);

function sendAxios(image: any, done: any) {
  let j = {
    image: image.asDataURL(),
    draw_image: {
      name: "init",
      path: "outputs/tmp",
      type: "png",
    },
  };

  // save to store as well
  imgPtroStr.set(image.asDataURL(), true);

  axios({
    method: "post",
    url: apiSave,
    data: j,
    headers: { "Access-Control-Allow-Origin": "*" },
  }).then((response: { data: any }) => {
    console.log(response.data);
    done(false);
  });
}

// TODO, save on change
// function changeSaveToStore(image: any) {
//   console.log(image);
//   console.log(image.getHeight());
// }

const props = defineProps<{
  mode: string;
}>();

// TODO, maybe insert useStorage, either here on in the store to save default for subsequent sessions
// then add button to reset to default, need to be careful against custom value per page, like mode etc
const aiInput = ref(defaultFvsionModel);
aiInput.value.mode = props.mode as ModeEnum;

// to be made from props, i.e. based on parent view
const apiRoot = getAPI("");
const apiSave = getAPI("save-as-base64");

onMounted(() => {
  aiInput.value.uuid = uuidv4();

  const ptro = Painterro({
    id: "painterro",
    defaultSize: "512x512",
    defaultTool: "brush",
    // ['crop', 'line', 'arrow', 'rect', 'ellipse', 'brush', 'text', 'rotate', 'resize', 'save', 'open', 'close', 'undo', 'redo', 'zoomin', 'zoomout', 'bucket']
    hiddenTools: [
      "crop",
      "line",
      "arrow",
      "rect",
      "ellipse",
      "text",
      "rotate",
      "resize",
      // "save",
      // "open",
      "close",
      "undo",
      "redo",
      "zoomin",
      "zoomout",
      "bucket",
    ],
    saveHandler: sendAxios,
    // onChange: changeSaveToStore,
  });

  ptro.show();
});
</script>

<template>
  <div>
    <div class="text-xl text-primary font-extrabold">Painterro</div>
    <div>Sketch or Load Your Image Prompts Here</div>
  </div>

  <div class="fixed">
    <div id="painterro" style="width: 600px; height: 600px"></div>
  </div>
</template>
