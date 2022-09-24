<script setup lang="ts">
import { defaultFvsionModel, jobQueue, job } from "../stores";

const axios: any = inject("axios"); // inject axios
const { joblist } = storeToRefs(jobQueue());

axios.interceptors.request.use(
  function (config: any) {
    // Do something before request is sent
    console.log("Start Ajax Call");
    const j: job = { name: "test", status: "test" };
    joblist.value.push(j);
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
  <pre>{{ joblist }}</pre>
</template>
