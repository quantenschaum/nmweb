<script>
  import Bool from "./Bool.svelte";
  import { menu } from "./Menu.svelte";
  import { info } from "./Info.svelte";
  import { dev_state, wifiMode } from "./nm";
  import { get, post } from "./util";
  import WiFiIcon from "./WiFiIcon.svelte";
  import ChannelBadge from "./ChannelBadge.svelte";
  import SecurityBagde from "./SecurityBagde.svelte";
  import DeviceIcon from "./DeviceIcon.svelte";
  import IpBadge from "./IpBadge.svelte";

  export let dev = {};

  let ap, state, color, mode;
  $: {
    ap = dev.ap;
    mode = dev.Mode;
    state =
      dev.State == 100 && (dev.Speed || dev.Bitrate)
        ? (dev.Speed ?? dev.Bitrate / 1000) + "Mbps"
        : dev_state[dev.State] || dev.State;

    color = "badge-warning";
    if (dev.State == 10) color = "";
    if (dev.State == 100) color = "badge-success";
    if ([20, 120].includes(dev.State)) color = "badge-error";
  }

  function down() {
    post("/nm/down", { device: dev["path"] });
  }

  function ip2str(ip) {
    if (Array.isArray(ip)) {
      let hextets = [];
      for (let i = 0; i < 16; i += 2) {
        let chunk = (ip[i] << 8) | ip[i + 1];
        hextets.push(chunk.toString(16));
      }
      return hextets.join(":");
    }
    return [
      ip & 0xff,
      (ip >>> 8) & 0xff,
      (ip >>> 16) & 0xff,
      (ip >>> 24) & 0xff,
    ].join(".");
  }

  function getIP(path, setter) {
    if (!path || path == "/") return;
    get("/nm/ip?path=" + path, (d) => {
      console.log(d);
      let a = "";
      a += d.Addresses.map((e) => `inet ${ip2str(e[0])}/${e[1]}`).join("\n");
      if (d.Gateway) a += `\ngateway ${d.Gateway}`;
      if (d.Nameservers) a += "\ndns " + d.Nameservers.map(ip2str).join(",");
      if (d.Domains) a += "\ndomains " + d.Domains.join(",");
      // console.log(a);
      setter(a);
    });
  }

  function del() {
    if (!window.confirm(`Delete device ${dev.Interface}?`)) return;
    post("/nm/delete", dev["path"]);
  }

  function ipInfo4() {
    getIP(dev.Ip4Config, (t) => info("IPv4 config", `<pre>${t}</pre>`));
  }
  function ipInfo6() {
    getIP(dev.Ip6Config, (t) => info("IPv6 config", `<pre>${t}</pre>`));
  }

  function showmenu(evt) {
    if (dev.Interface == "lo") return;
    menu(
      [
        ["Show IPv4", ipInfo4],
        ["Show IPv6", ipInfo6],
        ["Disconnect", down, "text-warning"],
        ["Delete", del, "text-error"],
      ],
      evt,
    );
  }
</script>

<tr on:contextmenu={showmenu}>
  <td>
    {#if ap}
      <WiFiIcon {ap} hotspot={mode == 3} />
    {:else}
      <DeviceIcon {dev} />
    {/if}
  </td>
  <td>{dev.Interface}</td>
  <!-- <td class="max-md:hidden">{dev.HwAddress}</td> -->
  <td class="max-sm:hidden">{dev.connection}</td>
  <td>
    <div class="badge badge-soft {color}">{state}</div>
    <ChannelBadge {ap} />
    <SecurityBagde {ap} />
    {#if mode && mode != 2}
      <div class="badge badge-soft badge-primary">{wifiMode[mode]}</div>
    {/if}
  </td>
  <td class="max-md:hidden"><Bool value={dev.Autoconnect} /></td>
  <td class="max-lg:hidden"><IpBadge mode={dev.Ip4Connectivity} /></td>
  <td class="max-lg:hidden"><IpBadge mode={dev.Ip6Connectivity} /></td>
</tr>
<!-- <pre>{JSON.stringify(dev, null, 2)}</pre> -->
