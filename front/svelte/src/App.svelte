<script lang="ts">
  let count = $state(0);
</script>
<main>
  <h1>Svelte playground</h1>
  <button onclick={() => count++}>count: {count}</button>
</main>
