<script>
  import Bool from "./Bool.svelte";
  import DeviceIcon from "./DeviceIcon.svelte";
  import IpBadge from "./IpBadge.svelte";
  import { menu } from "./Menu.svelte";
  import { edit } from "./Settings.svelte";
  import WiFiIcon from "./WiFiIcon.svelte";
  import { con_state, ETHERNET, pmfMode, WIRELESS, WIRELESS_SEC } from "./nm";
  import { get, post } from "./util";
  export let con = {};
  let state, ap, color, multi;
  let autocon, prio;
  let mac, key, pmf, mode, proto, group, pair;
  $: {
    ap = con.ap;
    let s = con.State;
    autocon = con.connection?.autoconnect ?? true;
    prio = con.connection?.["autoconnect-priority"];
    state = con_state[s] || s;
    color = "";
    if (s == 2) color = "badge-success";
    if ([1, 3, 4].includes(s)) color = "badge-warning";
    mac =
      con[WIRELESS]?.["assigned-mac-address"] ||
      con[ETHERNET]?.["assigned-mac-address"];
    key = con[WIRELESS_SEC]?.["key-mgmt"]?.toUpperCase();
    proto = con[WIRELESS_SEC]?.proto?.join(",").toUpperCase();
    group = con[WIRELESS_SEC]?.group?.join(",").toUpperCase();
    pair = con[WIRELESS_SEC]?.pairwise?.join(",").toUpperCase();
    pmf = con[WIRELESS_SEC]?.pmf;
    if (pmf) pmf = "pmf=" + pmfMode[pmf];
    mode = con[WIRELESS]?.mode?.toUpperCase();
    if (mode?.includes("INFRA")) mode = null;
    multi = con.connection?.["multi-connect"];
  }

  function up() {
    post("/nm/up", con.path);
  }

  function down() {
    if (!con.active) return;
    post("/nm/down", { connection: con.active });
  }

  function del() {
    if (!window.confirm(`Delete connection ${con.connection.id}?`)) return;
    post("/nm/delete", con.path);
  }

  function showEditor() {
    get("/nm/connection?path=" + con.path, (s) => {
      edit(s, (d) => post("/nm/update", d));
    });
  }

  function showmenu(evt) {
    if (con.connection?.id == "lo") return;
    menu(
      [
        ["Deactivate", down, "text-warning"],
        ["Edit", showEditor],
        ["Delete", del, "text-error"],
      ],
      evt,
    );
  }
</script>

<tr on:contextmenu={showmenu} on:dblclick={up} title="double click to activate">
  <td>
    {#if ap}
      <WiFiIcon {ap} hotspot={mode == "AP"} />
    {:else}
      <DeviceIcon dev={con} />
    {/if}
  </td>
  <td>{con.connection.id}</td>
  <td>{con.connection?.["interface-name"]}</td>
  <td class="max-lg:hidden">{mac}</td>
  <td>
    <div class="badge badge-soft {color}">
      {state}
    </div>
  </td>
  <td class="max-md:hidden">
    {#if key}
      <div
        class="badge badge-soft badge-secondary"
        title="{proto} {group} {pair} {pmf}"
      >
        {key}
      </div>
    {/if}
    {#if mode}
      <div class="badge badge-soft badge-primary">{mode}</div>
    {/if}
    {#if multi > 1}
      <div class="badge badge-soft badge-primary">multi</div>
    {/if}
  </td>
  <td class="max-md:hidden">
    <Bool value={autocon} title={prio} />
  </td>
  <td class="max-lg:hidden">
    <IpBadge mode={con.ipv4?.method} />
  </td>
  <td class="max-lg:hidden">
    <IpBadge mode={con.ipv6?.method} />
  </td>
</tr>
<!-- <pre>{JSON.stringify(con, null, 2)}</pre> -->
