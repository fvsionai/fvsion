<script setup lang="ts">
import { useJobQueue, job } from "../stores";

const axios: any = inject("axios"); // inject axios
const jobQueueStr = useJobQueue();

axios.interceptors.request.use(
  function (config: any) {
    // Do something before request is sent
    console.log("Start Ajax Call");
    console.log(config);

    const j: job = {
      name: "test",
      status: "test",
      prompt: config.data.prompt,
      uuid: config.data.uuid,
    };

    jobQueueStr.add(j);
    return config;
  },
  function (error: any) {
    // Do something with request error
    console.log("Error");
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  function (response: any) {
    // Do something with response data
    console.log("Done with Ajax call");
    return response;
  },
  function (error: any) {
    // Do something with response error
    console.log("Error fetching the data");
    return Promise.reject(error);
  }
);
</script>

<template>
  <div>
    <div class="font-bold">Job List</div>
    <div v-for="(j, index) in jobQueueStr.joblist">
      <span> {{ index }} : {{ j }}</span>
    </div>
  </div>
</template>
