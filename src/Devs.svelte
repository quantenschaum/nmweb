<script>
  import { onMount } from "svelte";
  import Device from "./Device.svelte";
  import { get } from "./util";
  import Info from "./Info.svelte";

  let devices = null;
  let error = null;

  function update() {
    error = null;
    get(
      "/nm/devices",
      (d) => (devices = d),
      (e) => (error = e.message),
    );
  }

  export let interval = 3;
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
      <th>type</th>
      <th>interface</th>
      <!-- <th class="max-md:hidden">mac</th> -->
      <th class="max-sm:hidden">connection</th>
      <th>state</th>
      <th class="max-md:hidden">auto</th>
      <th class="max-lg:hidden">IPv4</th>
      <th class="max-lg:hidden">IPv6</th>
    </tr>
  </thead>
  <tbody>
    {#each devices as dev}
      <Device {dev} />
    {/each}
  </tbody>
</table>

<Info />
