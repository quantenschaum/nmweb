<script>
  import { onMount } from "svelte";
  import Ap from "./Ap.svelte";
  import { get } from "./util";

  let connections = null;
  let error = null;

  function update() {
    error = null;
    get(
      "/nm/accesspoints",
      (d) => (connections = d),
      (e) => (error = e.message),
    );
  }

  export let interval = 5;
  onMount(() => {
    update();
    const timer = setInterval(update, 1000 * interval);
    return () => clearInterval(timer);
  });
</script>

{#if error}
  <div class="badge badge-error">{error}</div>
{/if}
<table class="table table-zebra" class:error>
  <thead>
    <tr>
      <th>sig</th>
      <th>name</th>
      <th>interface</th>
      <th class="max-md:hidden">mac</th>
      <th>channel</th>
      <th class="max-sm:hidden">security</th>
    </tr>
  </thead>
  <tbody>
    {#each connections as ap}
      <Ap {ap} />
    {/each}
  </tbody>
</table>
