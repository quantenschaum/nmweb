<script>
  import { secFlags, secModes } from "./nm";
  let security, color, mode;

  export let ap;

  let modes;

  function col(m) {
    if (m == "WPA3") return "badge-success";
    else if (m == "WPA2") return "badge-warning";
    else if (m == "open") return "badge-secondary";
    return "badge-error";
  }

  function info(m) {
    return secFlags(m == "WPA" ? ap.WpaFlags : ap.RsnFlags).join(",");
  }

  $: if (ap) {
    modes = secModes(ap.Flags, ap.WpaFlags, ap.RsnFlags);
  }
</script>

{#if ap}
  {#each modes as m}
    <div class="badge badge-soft {col(m)}" title={info(m)}>{m}</div>
  {/each}
{/if}
