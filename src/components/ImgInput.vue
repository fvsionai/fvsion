<script setup lang="ts">

const props = defineProps<{
  mode: string;
}>();
</script>

<template>
  <div>
    <form> 
    <label class="block">
      <span class="sr-only">Choose File</span>
      <input type="file" class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"/>
    </label>
  </form> 

    <!-- <input type="file" placeholder="ouputs/tmp/input.png" class="input  w-full" /> -->
    <!-- <input type="text" placeholder="ouputs/tmp/input.png" class="input input-bordered input-primary w-full" v-model="aiInput.file.name"/> -->
    
        <!-- <input class="form-control
    block
    w-full
    px-3
    py-1.5
    text-base
    font-normal
    text-gray-700
    bg-white bg-clip-padding
    border border-solid border-gray-300
    rounded
    transition
    ease-in-out
    m-0
    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none" type="file" id="formFile"> -->
      </div>
</template>