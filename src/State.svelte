<script>
  import { onMount } from "svelte";
  import { nm_state } from "./nm";
  import Icon from "@iconify/svelte";
  import disc from "@iconify-icons/mdi/local-area-network-disconnect";
  import conn from "@iconify-icons/mdi/local-area-network-connect";
  import pend from "@iconify-icons/mdi/local-area-network-pending";
  import won from "@iconify-icons/mdi/wifi-strength-outline";
  import woff from "@iconify-icons/mdi/wifi-strength-off-outline";
  import mon from "@iconify-icons/mdi/network-strength-outline";
  import moff from "@iconify-icons/mdi/network-strength-off-outline";
  import { get } from "./util";

  const concol = {
    0: "",
    1: "text-error",
    2: "text-primary",
    3: "text-warning",
    4: "text-success",
  };
  const consym = {
    0: disc,
    1: disc,
    2: pend,
    3: pend,
    4: conn,
  };

  let state = null;
  let error = null;

  function update() {
    error = null;
    get(
      "/nm/state",
      (d) => (state = d),
      (e) => (error = e.message),
    );
  }

  export let interval = 2;
  onMount(() => {
    update();
    const timer = setInterval(update, 1000 * interval);
    return () => clearInterval(timer);
  });

  let con, col, sym, ani;
  let wifi, wstate, wsym, wcol;
  let wwan, mstate, msym, mcol;
  $: if (state) {
    let enabled = state.NetworkingEnabled;
    let c = state.Connectivity;
    con = enabled ? nm_state[state.State] : "disabled";
    col = concol[c];
    sym = consym[c];
    ani = con.includes("ing") ? "animate-pulse" : null;

    wifi = (state.RadioFlags & 1) > 0;
    wwan = (state.RadioFlags & 2) > 0;

    let w = state.WirelessEnabled;
    let wh = state.WirelessHardwareEnabled;
    wsym = w && wh ? won : woff;
    wcol = w && wh ? "text-success" : "text-error";
    wstate = !wh ? "hard-off" : !w ? "soft-off" : "on";

    let m = state.WwanEnabled;
    let mh = state.WwanHardwareEnabled;
    msym = m && mh ? mon : moff;
    mcol = m && mh ? "text-success" : "text-error";
    mstate = !mh ? "hard-off" : !m ? "soft-off" : "on";
  }

  function toggle(radio) {
    if (radio == "w") radio = "WirelessEnabled";
    if (radio == "m") radio = "WwanEnabled";
    fetch("/nm/enable", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [radio]: !state[radio] }),
    }).catch(console.error);
  }
  let wtoggle = () => toggle("w");
  let mtoggle = () => toggle("m");
</script>

{#if error}
  <div class="badge badge-error">{error}</div>
{/if}
<div class="stats" class:error>
  <div class="stat place-items-center">
    <div class="stat-title">Connectivity</div>
    <div class="stat-value {col}">
      <Icon icon={sym} class="size-10 {ani}" />
    </div>
    <div class="stat-desc {col}">{con}</div>
  </div>
  {#if wifi}
    <div
      class="stat place-items-center"
      title="click to toggle"
      on:click={wtoggle}
    >
      <div class="stat-title">WiFi</div>
      <div class="stat-value {wcol}">
        <Icon icon={wsym} class="size-10" />
      </div>
      <div class="stat-desc {wcol}">{wstate}</div>
    </div>
  {/if}
  {#if wwan}
    <div
      class="stat place-items-center"
      title="click to toggle"
      on:click={mtoggle}
    >
      <div class="stat-title">WWan</div>
      <div class="stat-value {mcol}">
        <Icon icon={msym} class="size-10" />
      </div>
      <div class="stat-desc {mcol}">{mstate}</div>
    </div>
  {/if}
</div>
<!-- <pre>{JSON.stringify(state, null, 2)}</pre> -->
