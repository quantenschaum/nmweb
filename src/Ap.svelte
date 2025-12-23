<script>
  import { post } from "./util";
  import ChannelBadge from "./ChannelBadge.svelte";
  import WiFiIcon from "./WiFiIcon.svelte";
  import SecurityBagde from "./SecurityBagde.svelte";

  export let ap = {};

  function connect() {
    let passwd;
    if (ap.Flags) passwd = window.prompt(`Password for ${ap.ssid}`);
    if (ap.Flags && !passwd) return;
    post("/nm/connect", {
      path: ap.path,
      dev: ap.dev,
      psk: passwd,
    });
  }
</script>

<tr on:dblclick={connect} title="double click to connect">
  <td><WiFiIcon {ap} /></td>
  <td>{ap.ssid}</td>
  <td>{ap.ifname}</td>
  <td class="max-md:hidden">{ap.HwAddress}</td>
  <td><ChannelBadge {ap} /></td>
  <td class="max-sm:hidden"><SecurityBagde {ap} /></td>
</tr>
<!-- <pre>{JSON.stringify(ap, null, 2)}</pre> -->
