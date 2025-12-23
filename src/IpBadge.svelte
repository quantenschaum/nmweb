<script>
  import { connectivity } from "./nm";

  export let mode;

  const colors = {
    // device modes
    1: "badge-error",
    2: "badge-primary",
    3: "badge-warning",
    4: "badge-success",
    // connection modes
    auto: "badge-success",
    manual: "badge-warning",
    disabled: "badge-error",
    shared: "badge-accent",
  };

  let color, name;
  $: if (mode != null) {
    color = colors[mode];
    name = connectivity[mode] || mode;
  }
</script>

{#if mode != null}
  <div class="badge badge-soft {color}">{name}</div>
{/if}
