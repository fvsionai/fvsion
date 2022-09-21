<script lang="ts" setup>
const isCheck = true; //TODO: do some check
const reRoute = computed(() => {
  if (isCheck)
    return {
      to: "/",
      text: "Go Home",
    };
  return {
    to: "/signin",
    text: "Sign In",
  };
});
</script>
<template>
  <div class="mb-4 self-center text-xl font-medium">404 - Page not found</div>
  <router-link :to="reRoute.to" class="btn btn-primary self-center">{{ reRoute.text }}</router-link>
</template>
