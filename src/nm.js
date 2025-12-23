export const ETHERNET = "802-3-ethernet";
export const WIRELESS = "802-11-wireless";
export const WIRELESS_SEC = "802-11-wireless-security";

export const dev_state = {
  0: "unknown",
  10: "unmanaged",
  20: "unavailable",
  30: "disconnected",
  40: "prepare",
  50: "config",
  60: "need auth",
  70: "ip config",
  80: "ip check",
  90: "secondaries",
  100: "connected",
  110: "deactivating",
  120: "failed",
};

export const con_state = {
  0: "unknown",
  1: "activating",
  2: "connected",
  3: "deactivating",
  4: "deactivated",
  5: "inactive",
};

export const dev_type = {
  0: "unknown",
  1: "ethernet",
  2: "WiFi",
  5: "BT",
  10: "bond",
  13: "bridge",
  14: "generic",
  16: "tun",
  29: "wireguard",
  30: "WiFi P2P",
  32: "loopback",
};

export const connectivity = {
  0: "unknown",
  1: "none",
  2: "portal",
  3: "limited",
  4: "full",
};

export const nm_state = {
  0: "unknown",
  10: "asleep",
  20: "disconnected",
  30: "disconnecting",
  40: "connecting",
  50: "local",
  60: "site",
  70: "global",
};

export const wifiMode = {
  0: "unknown",
  1: "ADHOC",
  2: "INFRA",
  3: "AP",
  4: "MESH",
};

export function apFlags(flags) {
  let a = [];
  if (flags & 0x1) a.push("PRIV");
  if (flags & 0x2) a.push("WPS");
  if (flags & 0x4) a.push("PBC");
  if (flags & 0x8) a.push("PIN");
  return a;
}

export function secFlags(flags) {
  let a = [];
  if (flags & 0x1) a.push("p:WEP40");
  if (flags & 0x2) a.push("p:WEP104");
  if (flags & 0x4) a.push("p:TKIP");
  if (flags & 0x8) a.push("p:CCMP");

  if (flags & 0x10) a.push("g:WEP40");
  if (flags & 0x20) a.push("g:WEP104");
  if (flags & 0x40) a.push("g:TKIP");
  if (flags & 0x80) a.push("g:CCMP");

  if (flags & 0x100) a.push("PSK");
  if (flags & 0x200) a.push("802-1X");
  if (flags & 0x400) a.push("SAE");
  if (flags & 0x800) a.push("OWE");
  if (flags & 0x1000) a.push("OWE-TM");
  if (flags & 0x2000) a.push("EAP");
  return a;
}

export const pmfMode = {
  0: "default",
  1: "disable",
  2: "optional",
  3: "required",
};

export function secModes(ap, wpa, rsn) {
  let sec;
  if (ap == 0) sec = ["open"];
  if (ap > 0) sec = ["WEP"];
  if (wpa || rsn) sec = [];
  if (wpa) sec.push("WPA");
  let psk = rsn & 0x100;
  let sae = rsn & 0x400;
  if (rsn && psk) sec.push("WPA2");
  if (rsn && sae) sec.push("WPA3");
  return sec;
}
