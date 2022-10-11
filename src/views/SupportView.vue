<script setup lang="ts">
import Kofi from "@/components/Kofi.vue";
</script>

<template>
  <h1 class="text-3xl font-medium">Support</h1>

  <div class="not-prose">
    <p>You can support me, the developer for Fvsion App by;</p>
    <ul class="list-disc">
      <li>sharing about this tools on forums and social media</li>
      <li>
        suggesting features and even better create a Pull Request for new
        features at
        <a
          href="https://github.com/FvsionAI/fvsion"
          class="text-primary"
          target="_blank"
          >github.com/FvsionAI/fvsion</a
        >
      </li>
      <li>
        direct donation via
        <a href="https://ko-fi.com/hafiidz" target="_blank"
          >ko-fi.com/hafiidz</a
        >
        <br />
        <Kofi></Kofi>
      </li>
    </ul>

    <p>Every little bit helps. Thanks in advance.</p>
  </div>
</template>
