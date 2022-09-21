<script setup lang="ts">
import axios, { AxiosResponse } from "axios";
import { reactive } from "vue";

const state = reactive({ myPID: "Click get PID to retrieve." });

async function getPID() {
  try {
    const response = await axios.get("http://127.0.0.1:4242/pid");
    console.log(response);
    // console.log(response.data);
    if (response.status == 200) {
      success(response);
    }
  } catch (error) {
    console.error(error);
  }
}

function success(res: AxiosResponse) {
  state.myPID = "FastAPI PID is " + res.data.pid;
  console.log(state.myPID);
}
</script>

<template>
  <div>
    <span> {{ state.myPID }} </span>
  </div>
  <div><button @click="getPID" class="btn btn-primary text-gray-900 bg-red-500">get PID</button></div>
</template>
