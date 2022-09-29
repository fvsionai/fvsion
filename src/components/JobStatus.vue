<script setup lang="ts">
import { useJobQueue, job } from "../stores";
import customAxios from "@/utils/custom.axios";

const jobQueueStr = useJobQueue();

customAxios.interceptors.request.use(
  function (config: any) {
    // Do something before request is sent
    console.log("Start Ajax Call");

    const j: job = {
      status: "submitted",
      prompt: config.data.prompt,
      uuid: config.data.uuid,
    };

    jobQueueStr.add(j);
    return config;
  },
  function (error: any) {
    // Do something with request error
    console.log("Error");
    console.log(error);

    return Promise.reject(error);
  }
);

customAxios.interceptors.response.use(
  function (response: any) {
    // Do something with response data
    console.log("Done with Ajax call");

    const j: job = {
      status: "completed",
      prompt: response.data.prompt,
      uuid: response.data.uuid,
    };

    jobQueueStr.update(j);
    return response;
  },
  function (error: any) {
    // Do something with response error
    console.log("Error fetching the data");
    // console.log(error);
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
