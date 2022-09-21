<script setup lang="ts">
const schema = [
  {
    $formkit: "prompt",
    label: "Prompt",
  },
];

const JSONschema = {
  title: "FvsionModel",
  type: "object",
  properties: {
    prompt: { title: "Prompt", type: "string" },
    height: { title: "Height", default: 512, type: "integer" },
    width: { title: "Width", default: 512, type: "integer" },
    num_inference_steps: {
      title: "Num Inference Steps",
      default: 16,
      type: "integer",
    },
    guidance_scale: {
      title: "Guidance Scale",
      default: 7.5,
      type: "number",
    },
    eta: { title: "Eta", default: 0.0, type: "number" },
    seed: { title: "Seed", default: 1024, type: "integer" },
    allowNSFW: { title: "Allownsfw", default: true, type: "boolean" },
  },
  required: ["prompt"],
};
</script>

<template>
  <FormKit type="form">
    <FormKitSchema :schema="schema" />
  </FormKit>
</template>
