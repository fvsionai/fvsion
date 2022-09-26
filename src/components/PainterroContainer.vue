<script setup lang="ts">
import Painterro from "painterro";
import { defaultFvsionModel } from "../stores";
import { getAPI } from "../utils";
import { v4 as uuidv4 } from "uuid";

const axios: any = inject("axios"); // inject axios

function sendAxios(image: any, done: any) {
  aiInput.value.uuid = uuidv4();
  let j = {
    image: image.asDataURL(),
    draw_image: {
      name: "test2",
      path: "output",
      type: "png",
    },
  };

  console.log(j);

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

const props = defineProps<{
  mode: string;
}>();

// TODO, maybe insert useStorage, either here on in the store to save default for subsequent sessions
// then add button to reset to default, need to be careful against custom value per page, like mode etc
const aiInput = ref(defaultFvsionModel);
aiInput.value.mode = props.mode;

// to be made from props, i.e. based on parent view
const apiRoot = getAPI("");
const apiSave = getAPI("save-as-base64");

onMounted(() => {
  Painterro({
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
      "open",
      "close",
      "undo",
      "redo",
      "zoomin",
      "zoomout",
      "bucket",
    ],
    saveHandler: sendAxios,
  }).show();
});
</script>

<template>
  <div class="fixed">
    <div id="painterro" style="width: 600px; height: 600px"></div>
  </div>
</template>
