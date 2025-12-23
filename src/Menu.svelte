<script context="module">
  import { writable } from "svelte/store";

  const menudata = writable();

  export function menu(items, event) {
    event.preventDefault();
    menudata.set({ items, x: event.clientX, y: event.clientY });
  }
</script>

<script>
  import { onMount } from "svelte";

  const close = () => ($menudata = null);

  onMount(() => {
    window.addEventListener("click", close);
    return () => window.removeEventListener("click", close);
  });
</script>

{#if $menudata}
  <ul
    class="menu dropdown-content bg-base-100 rounded-box p-2 shadow-lg fixed z-50"
    style="top: {$menudata.y}px; left: {$menudata.x}px;"
  >
    {#each $menudata.items as i}
      <li on:click={i[1]} class={i[2]}><a>{@html i[0]}</a></li>
    {/each}
  </ul>
{/if}
