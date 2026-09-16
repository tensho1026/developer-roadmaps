<script setup lang="ts">
import { useCounter } from "./store";
const counter = useCounter();
</script>
<template>
  <main class="p-8">
    <h1 class="text-2xl font-bold">Vue playground</h1>
    <p>Vue Router / Pinia / Tailwind</p>
    <button class="mt-4 border px-3 py-2" @click="counter.inc">count: {{ counter.count }}</button>
  </main>
</template>
