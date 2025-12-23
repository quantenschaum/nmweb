<script>
  import Icon from "@iconify/svelte";
  import ether from "@iconify-icons/mdi/ethernet";
  import loop from "@iconify-icons/mdi/loop";
  import lan from "@iconify-icons/mdi/lan";
  import wifi from "@iconify-icons/mdi/wifi";
  import wifil from "@iconify-icons/mdi/wifi-lock";
  import bridge from "@iconify-icons/mdi/bridge";
  import bluetooth from "@iconify-icons/mdi/bluetooth";
  import vpn from "@iconify-icons/mdi/vpn";
  import { dev_type } from "./nm";

  export let dev;

  let color, icon, type;
  $: if (dev) {
    // devices
    type = dev.DeviceType;
    if (type) {
      color = null;
      if (dev.State == 100) color = "text-info";
      if (dev.primary) color = "text-accent";

      icon = lan;
      if (type == 1) icon = ether;
      if (type == 2) icon = wifi;
      if (type == 30) icon = wifi;
      if (type == 13) icon = bridge;
      if (type == 32) icon = loop;
      if (type == 29) icon = vpn;

      type = dev_type[type] || type;
    } else {
      // connections
      type = dev.connection?.type ?? "";
      if (type) {
        color = "";
        if (dev.State == 2) color = "text-info";
        if (dev.primary) color = "text-accent";

        icon = lan;
        if (type.includes("ethernet")) icon = ether;
        if (type.includes("wireless")) icon = wifi;
        if (type.includes("loop")) icon = loop;
        if (type.includes("vpn")) icon = vpn;
        if (type.includes("wireguard")) icon = vpn;
        if (type.includes("bridge")) icon = bridge;
        if (type.includes("bluetooth")) icon = bluetooth;
        if (type == wifi && dev["802-11-wireless"]?.security) icon = wifil;
      }
    }
  }
</script>

{#if dev}
  <div class={color} title={type}>
    <Icon {icon} class="size-6" />
  </div>
{/if}
