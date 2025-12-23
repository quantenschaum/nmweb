<script>
  export let ap;
  let channel, freq, bw, maxrate, color;
  $: if (ap) {
    let f = ap.Frequency;
    freq = f / 1000;
    if (f > 5000) channel = (f - 5000) / 5;
    else channel = (f - 2407) / 5;
    bw = ap.Bandwidth;
    maxrate = ap.MaxBitrate / 1000;
    if (freq > 3) color = "badge-info";
    else color = "badge-primary";
  }
</script>

{#if ap}
  <div class="badge badge-soft {color}" title="{freq}GHz {bw}MHz {maxrate}kbps">
    {channel}
  </div>
{/if}
