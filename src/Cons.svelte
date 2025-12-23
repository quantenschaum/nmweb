<script>
  import { onMount } from "svelte";
  import Connection from "./Connection.svelte";
  import { get } from "./util";
  import Settings from "./Settings.svelte";

  let connections = null;
  let error = null;

  function update() {
    error = null;
    get(
      "/nm/connections",
      (d) => (connections = d),
      (e) => (error = e.message),
    );
  }

  export let interval = 4;
  onMount(() => {
    update();
    const timer = setInterval(update, 1000 * interval);
    return () => clearInterval(timer);
  });

  let editor, settings, apply;
  function edit(sets, save) {
    settings = sets;
    apply = (s) => {
      save(s);
      editor.close();
    };
    editor.showModal();
  }
</script>

{#if error}
  <div class="badge badge-error">{error}</div>
{/if}
<table class="table table-zebra" class:error>
  <thead>
    <tr>
      <th>type</th>
      <th>connection</th>
      <th>interface</th>
      <th class="max-lg:hidden">mac</th>
      <th>state</th>
      <th class="max-md:hidden">flags</th>
      <th class="max-md:hidden">auto</th>
      <th class="max-lg:hidden">IPv4</th>
      <th class="max-lg:hidden">IPv6</th>
    </tr>
  </thead>
  <tbody>
    {#each connections as con}
      <Connection {con} {edit} />
    {/each}
  </tbody>
</table>

<Settings />
