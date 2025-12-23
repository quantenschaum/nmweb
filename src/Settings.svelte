<script context="module">
  import { writable } from "svelte/store";
  const settings = writable();
  const apply = writable();
  export function edit(sets, aply) {
    console.log(sets, aply);
    settings.set(sets);
    apply.set(aply);
  }
</script>

<script>
  import _ from "lodash";
  import { get } from "./util";
  import { ETHERNET, WIRELESS, WIRELESS_SEC } from "./nm";
  let dialog;

  const bool = { yes: true, no: false };
  const number = "number";

  const types = {
    connection: {
      autoconnect: bool,
      "multi-connect": {
        default: 0,
        single: 1,
        "multi (manual)": 2,
        multi: 3,
      },
      permissions: false,
      timestamp: false,
      uuid: false, // hidden
      type: null, //disabled
      "slave-type": [null, "bridge"],
    },
    [ETHERNET]: {
      "s390-options": false,
      "assigned-mac-address": ["preserve", "permanent", "random", "stable"],
      "auto-negotiate": bool,
    },
    [WIRELESS]: {
      band: {
        auto: null,
        "2GHz": "bg",
        "5GHz": "a",
      },
      channel: number,
      "channel-width": false,
      // {        auto: 0,        "20MHz": 20,        "40MHz": 40,        "80MHz": 80,      },
      hidden: bool,
      "mac-address-randomization": false,
      mode: ["infrastructure", "adhoc", "ap", "mesh"],
      "ap-isolation": ["default", true, false],
      "assigned-mac-address": [
        null,
        "preserve",
        "permanent",
        "random",
        "stable",
        "stable-ssid",
      ],
      powersave: {
        default: 0,
        ignore: 1,
        disable: 2,
        enable: 3,
      },
      "seen-bssids": false,
      security: false,
    },
    [WIRELESS_SEC]: {
      preset: [null, "WPA", "WPA2", "WPA3"],
      "key-mgmt": ["none", "wpa-psk", "sae"],
      "auth-alg": [null, "open", "shared", "leap"],
      proto: [null, "wpa", "rsn", "wpa,rsn"],
      group: [null, "tkip", "ccmp", "tkip,ccmp"],
      pairwise: [null, "tkip", "ccmp", "tkip,ccmp"],
      pmf: {
        default: 0,
        disable: 1,
        optional: 2,
        required: 3,
      },
    },
    proxy: false,
    ipv4: {
      method: ["auto", "link-local", "manual", "shared", "disabled"],
      "may-fail": bool,
      forwarding: { default: -1, no: 0, yes: 1, auto: 2 },
    },
    ipv6: {
      method: [
        "ignore",
        "auto",
        "dhcp",
        "link-local",
        "manual",
        "shared",
        "disabled",
      ],
      "may-fail": bool,
      "addr-gen-mode": {
        eui64: 0,
        "stable-privacy": 1,
        "default-or-eui64": 2,
        default: 3,
      },
      "ip6-privacy": {
        default: -1,
        disabled: 0,
        "prefer-public-addr": 1,
        "prefer-temp-addr": 2,
      },
    },
  };

  function hidden(g, k) {
    if (types[g] === false) return true;
    return types[g]?.[k] === false;
  }
  function disabled(g, k) {
    if (types[g] === null) return true;
    return types[g]?.[k] === null;
  }
  function isBool(v) {
    return v === true || v === false;
  }
  function isSelect(g, k, v) {
    let t = types[g]?.[k];
    if (!t && isBool(v)) return true;
    return t != null && typeof t === "object";
  }
  function options(g, k, v) {
    let t = types[g]?.[k];
    if (!t && isBool(v)) t = bool;
    if (Array.isArray(t)) return t.map((v) => ({ name: v, value: v }));
    return Object.entries(t).map(([k, v]) => ({ name: k, value: v }));
  }
  function itype(g, k, v) {
    // if (k == "psk") return "password";
    if ((types[g]?.[k] || typeof v) === "number") return "number";
    return "text";
  }

  const common1 = {
    connection: {
      type: null,
      id: null,
      "interface-name": null,
      autoconnect: true,
      "autoconnect-priority": 0,
      // "autoconnect-retries": -1,
      "multi-connect": null,
      master: null,
      // "slave-type": null,
    },
  };
  const common2 = {
    ipv4: {
      method: "auto",
      "address-data": null,
      "dns-data": null,
      "dns-search": null,
      // gateway: null,
      // forwarding: null,
    },
    ipv6: { method: "auto", "addr-gen-mode": null },
  };
  const ethernet = {
    [ETHERNET]: {
      "assigned-mac-address": null,
      "auto-negotiate": true,
      // duplex: true,
      // speed: 0,
    },
  };
  const bridge = {
    bridge: {
      stp: false,
    },
  };
  const wifi = {
    [WIRELESS]: {
      ssid: [],
      mode: "infrastructure",
      band: null,
      channel: null,
      "channel-width": 0,
      "mac-address-randomization": 0,
      "assigned-mac-address": null,
      powersave: 0,
      security: WIRELESS_SEC,
    },
    [WIRELESS_SEC]: {
      preset: null,
      psk: null,
      "key-mgmt": null,
      proto: null,
      group: null,
      pairwise: null,
      pmf: null,
    },
  };

  function a2s(a) {
    return String.fromCharCode(...a);
  }
  function s2a(s) {
    return Array.from(s).map((c) => c.charCodeAt(0));
  }

  function addrIn(ad) {
    return ad.map((e) => `${e.address}/${e.prefix}`).join(",");
  }

  function addrOut(s) {
    return s.split(",").map((p) => {
      [addr, pref] = p.trim().split("/");
      return { address: addr, prefix: pref };
    });
  }

  function transformIn(settings) {
    // console.log(settings);
    let data = _.merge({}, common1);
    let type = settings?.connection?.type;
    if (type == WIRELESS) _.merge(data, wifi);
    if (type == ETHERNET) _.merge(data, ethernet);
    if (type == "bridge") _.merge(data, bridge);
    _.merge(data, common2, settings);
    let ssid = data?.[WIRELESS]?.ssid;
    if (ssid) data[WIRELESS].ssid = a2s(ssid);

    ["proto", "group", "pairwise"].forEach((k) => {
      let v = data[WIRELESS_SEC]?.[k];
      if (v) data[WIRELESS_SEC][k] = v.join(",");
    });

    function ipvx(ip) {
      if (!ip) return;
      let ad = ip?.["address-data"];
      if (ad) {
        ip["address-data"] = addrIn(ad);
      }
      let dns = ip?.["dns-data"];
      if (dns) {
        ip["dns-data"] = dns.join(",");
      }
      let search = ip?.["dns-search"];
      if (search) {
        ip["dns-search"] = search.join(",");
      }
      delete ip["addresses"];
      // delete ip["route-data"];
      // delete ip["dns-data"];
    }
    ipvx(data.ipv4);
    delete data?.connection?.timestamp;
    delete data?.[WIRELESS]?.["seen-bssids"];

    return data;
  }

  function isEmpty(v) {
    if (v == null) return true;
    if (v == "") return true;
    if (v === false) return false;
    return (_.isObject(v) || _.isArray(v)) && _.isEmpty(v);
  }

  function transformOut(data) {
    let out = _.merge({}, data);
    // let ssid = out?.[WIRELESS]?.ssid;
    // if (ssid) out[WIRELESS].ssid = s2a(ssid);
    // let proto = data[WIRELESS_SEC]?.proto.split(",");
    // if (proto) data[WIRELESS_SEC]?.proto=proto;
    // remove empty/default values
    delete out[WIRELESS_SEC].preset;
    out = _.mapValues(out, (g) => _.omitBy(g, (v, k) => isEmpty(v)));
    out = _.omitBy(out, (v, k) => isEmpty(v));
    // console.log(out);
    return out;
  }

  let devices = [];
  let bridges = [];
  $: {
    if ($settings)
      get("/nm/devices", (devs) => {
        let type = $settings?.connection?.type;
        let dtype = 0;
        if (type == ETHERNET) dtype = 1;
        if (type == WIRELESS) dtype = 2;
        devices = devs
          .filter((d) => d.DeviceType == dtype)
          .map((d) => d.Interface);
        bridges = devs
          .filter((d) => d.DeviceType == 13)
          .map((d) => d.Interface);
      });
  }

  let data;
  $: {
    types.connection["interface-name"] = _.isEmpty(devices)
      ? "text"
      : [null, ...devices];
    types.connection["master"] = _.isEmpty(bridges)
      ? false
      : [null, ...bridges];
    data = transformIn($settings);
  }

  $: types.connection["autoconnect-priority"] = data.connection?.["autoconnect"]
    ? number
    : false;

  $: {
    let mode = data[WIRELESS]?.mode;
    let sec = data[WIRELESS_SEC];
    let kmgmt = sec?.["key-mgmt"];

    // WPA3
    if (mode == "ap" && kmgmt == "sae") {
      sec.proto = "rsn";
      sec.group = "ccmp";
      sec.pairwise = "ccmp";
      sec.pmf = 3;
    }
  }

  const WPA = {
    WPA: ["wpa-psk", "wpa", "tkip", "tkip"],
    WPA2: ["wpa-psk", "rsn", "ccmp", "ccmp"],
    WPA3: ["sae", "rsn", "ccmp", "ccmp"],
  };

  $: {
    let sec = data[WIRELESS_SEC];
    let pre = sec?.preset;
    if (pre) [sec["key-mgmt"], sec.proto, sec.group, sec.pairwise] = WPA[pre];
  }

  const BAND = types[WIRELESS].band;
  $: if (data[WIRELESS]?.channel) {
    types[WIRELESS].band = null;
    data[WIRELESS].band = data[WIRELESS]?.channel > 14 ? "a" : "bg";
  } else {
    types[WIRELESS].band = BAND;
  }

  $: if ($settings) dialog.showModal();

  function save() {
    dialog.close();
    $apply(transformOut(data));
  }
</script>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box max-w-3/4">
    <form method="dialog">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
        ✕
      </button>
    </form>
    {#each Object.entries(data) as [group, $settings]}
      {#if !hidden(group)}
        <fieldset
          class="fieldset bg-base-200 border-base-300 rounded-box border p-4"
        >
          <legend class="fieldset-legend">{group}</legend>
          {#each Object.entries($settings) as [key, value]}
            {#if hidden(group, key)}
              <!-- skip -->
            {:else if isSelect(group, key, value)}
              <label class="select w-full">
                <span class="label w-50">{key}</span>
                <select bind:value={data[group][key]}>
                  {#each options(group, key, value) as t}
                    <option value={t.value}>{t.name}</option>
                  {/each}
                </select>
              </label>
            {:else}
              <label class="input w-full">
                <span class="label w-50">{key}</span>
                <input
                  type={itype(group, key, value)}
                  bind:value={data[group][key]}
                  disabled={disabled(group, key)}
                />
              </label>
            {/if}
            <!-- <pre class="text-sx">{group}.{key}={JSON.stringify(
            data[group][key],
          )}</pre> -->
          {/each}
        </fieldset>
      {/if}
    {/each}
    <button class="btn btn-accent mt-4 w-full" on:click={save}>Save</button>
  </div>
</dialog>
