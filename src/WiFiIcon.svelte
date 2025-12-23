<script>
  import Icon from "@iconify/svelte";
  import wifi0 from "@iconify-icons/mdi/wifi-strength-0";
  import wifi1 from "@iconify-icons/mdi/wifi-strength-1";
  import wifi2 from "@iconify-icons/mdi/wifi-strength-2";
  import wifi3 from "@iconify-icons/mdi/wifi-strength-3";
  import wifi4 from "@iconify-icons/mdi/wifi-strength-4";

  import wifi0l from "@iconify-icons/mdi/wifi-strength-0-lock";
  import wifi1l from "@iconify-icons/mdi/wifi-strength-1-lock";
  import wifi2l from "@iconify-icons/mdi/wifi-strength-2-lock";
  import wifi3l from "@iconify-icons/mdi/wifi-strength-3-lock";
  import wifi4l from "@iconify-icons/mdi/wifi-strength-4-lock";

  export let ap, hotspot;

  let icon, color, strength;
  $: if (ap) {
    strength = hotspot ? 100 : ap.Strength;
    let open = !ap.Flags;
    if (strength > 80) icon = open ? wifi4 : wifi4l;
    else if (strength > 60) icon = open ? wifi3 : wifi3l;
    else if (strength > 40) icon = open ? wifi2 : wifi2l;
    else if (strength > 20) icon = open ? wifi1 : wifi1l;
    else icon = open ? wifi0 : wifi0l;

    if (strength > 80) color = "text-teal-500";
    else if (strength > 60) color = "text-green-600";
    else if (strength > 40) color = "text-yellow-600";
    else if (strength > 20) color = "text-orange-600";
    else color = "text-red-600";
    // color = "text-primary ";
  }
</script>

{#if ap}
  <div class={color} title="{strength}%">
    <Icon {icon} class="size-6" />
  </div>
{/if}
