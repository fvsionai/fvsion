<script setup lang="ts">
import axios from "axios";
import fs from "fs";
import path from "path";
import FormData from "form-data";

// const props = defineProps<{
//   api: string;
// }>();

const imgur = "https://api.imgur.com/3/upload";
const img = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7";
const uploadImg = (e: any): void => {
  e.preventDefault();

  const pathToFile = path.join("outputs/tmp/init.png");

  const data = new FormData();
  data.append("image", fs.createReadStream(pathToFile));

  const config = {
    headers: {
      "Content-type": "application/x-www-form-urlencoded",
      Authorization: "Client-ID {{clientId}}",
    },
  };

  console.log(data);

  axios.post(imgur, data, config).then((response: { data: any }) => {
    console.log(response.data);
  });
};
</script>

<template>
  <form>
    <div>
      <input type="file" @change="uploadImg" id="img" />
      <button class="btn btn-primary" @click="uploadImg">Test</button>
    </div>
  </form>
</template>
