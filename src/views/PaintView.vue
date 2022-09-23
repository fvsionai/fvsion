<script setup lang="ts">
import Painterro from "painterro";

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
      "save",
      "open",
      "close",
      "undo",
      "redo",
      "zoomin",
      "zoomout",
      "bucket",
    ],
  }).show();
});
</script>

<template>
  <div class="relative">
    <div id="painterro" style="width: 800px; height: 600px"></div>
  </div>
</template>
