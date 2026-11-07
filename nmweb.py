#!/usr/bin/env python3
import time
from typing import Any, Dict, List, Optional

from flask import Flask, request, send_file, send_from_directory
from pydbus import SystemBus, Variant

try:
    from rich import print
except:
    pass

app = Flask(__name__)
bus = SystemBus()

nm_base = "org.freedesktop.NetworkManager"
nm_path = "/org/freedesktop/NetworkManager"

STATE_FIELDS = [
    "State",
    "NetworkingEnabled",
    "WirelessEnabled",
    "WirelessHardwareEnabled",
    "WwanEnabled",
    "WwanHardwareEnabled",
    "RadioFlags",
    "PrimaryConnection",
    "PrimaryConnectionType",
    "Version",
    "Connectivity",
    "ConnectivityCheckAvailable",
    "ConnectivityCheckEnabled",
    "ConnectivityCheckUri",
    "GlobalDnsConfiguration",
]

DEV_FIELDS = [
    "Interface",
    "State",
    "ActiveConnection",
    "Capabilities",
    "Managed",
    "Autoconnect",
    "DeviceType",
    "Ip4Connectivity",
    "Ip6Connectivity",
    "HwAddress",
    "Ip4Config",
    "Ip6Config",
    "Speed",
    "Carrier",
    "Bitrate",
    "Mode",
    "ActiveAccessPoint",
    "WirelessCapabilities",
]

AP_FIELDS = [
    "Flags",
    "WpaFlags",
    "RsnFlags",
    "Ssid",
    "Frequency",
    "HwAddress",
    "Mode",
    "MaxBitrate",
    "Bandwidth",
    "Strength",
    "LastSeen",
]

ACTIVE_CONNECTION_FIELDS = [
    "Connection",
    "Id",
    "Type",
    "Devices",
    "State",
]

IP_FIELDS = [
    "Addresses",
    "Gateway",
    "Domains",
    "Nameservers",
    "Searches",
    "DnsOptions",
    "DnsPriority",
]


@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/")
def root():
    return send_file("dist/index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory("dist", filename)


def nm(path=""):
    "access NM on dbus"
    path = path if path.startswith("/") else nm_path + "/" + path if path else nm_path
    return bus.get(nm_base, path)


def getfield(obj, field):
    "get attr from obj or None"
    try:
        return getattr(obj, field)
    except:
        return None


def getobj(path, fields) -> Dict[str, Any]:
    "get fields from dbus obj as dict"
    o = nm(path)
    d = {k: getfield(o, k) for k in fields}
    d["path"] = path
    return d


def dget(data, path, default=None):
    "get value from nested dicts with path like a.b.c"
    keys = path.split(".")
    for k in keys[:-1]:
        data = data.get(k, {})
    return data.get(keys[-1], default)


def dset(data, path, value):
    "set value in nested dicts on path like a.b.c"
    keys = path.split(".")
    for k in keys[:-1]:
        data = data.setdefault(k, {})
    data[keys[-1]] = value


@app.route("/nm/state")
def state() -> Dict[str, Any]:
    "NM connection state"
    return getobj("", STATE_FIELDS)


def primary() -> Optional[str]:
    "path of primary connection or None"
    p = nm().PrimaryConnection
    return p if len(p) > 1 else None


def devices() -> List[Dict[str, Any]]:
    "list of device properties with additional infos"
    pri = primary()
    devs = []
    for p in nm().Devices:
        dev = getobj(p, DEV_FIELDS)
        ac = dev["ActiveConnection"]
        dev["primary"] = ac == pri
        dev["connection"] = nm(ac).Id if len(ac) > 1 else None
        aap = dev["ActiveAccessPoint"]
        dev["ap"] = ap(aap) if aap else None
        devs.append(dev)
        # print(dev)
    return devs


@app.route("/nm/devices")
def devs():
    return sorted(
        devices(),
        key=lambda d: 0 if d["primary"] else 1 if d["connection"] else 2,
    )


def active_connections() -> Dict[str, Dict]:
    "get active connections"
    cons = {}
    for p in nm().ActiveConnections:
        con = getobj(p, ACTIVE_CONNECTION_FIELDS)
        cons[con["Connection"]] = con
    return cons


def getAP(aps, ssid, ifname):
    m = list(
        filter(
            lambda a: a["Ssid"] == ssid and (not ifname or ifname == a["ifname"]),
            aps,
        )
    )
    if m:
        return m[0]


def connections() -> List[Dict[str, Any]]:
    "connection settings with additional information like state, primary"
    pri = primary()
    acs = active_connections()
    aps = accesspoints()
    cons = []
    for p in nm("Settings").Connections:
        con = settings(p)
        con["path"] = p
        ac = acs.get(p, {})
        con["State"] = ac.get("State", 5)
        con["primary"] = pri and ac.get("path") == pri
        con["active"] = ac.get("path")
        ifname = dget(con, "connection.interface-name")
        ssid = dget(con, "802-11-wireless.ssid")
        con["ap"] = getAP(aps, ssid, ifname)
        if con["ap"]:  # update TS to push connection up in list sort
            dset(con, "connection.timestamp", int(time.time()) + 100)
        cons.append(con)
        # print(con)
    return cons


@app.route("/nm/connections")
def cons():
    return sorted(
        connections(),
        key=lambda c: (
            -(1000 if c["primary"] else 1)
            * (c["State"] % 5 or 1)
            * dget(c, "connection.timestamp", 0)
        ),
    )


def ap(path, dev=None) -> Optional[Dict[str, Any]]:
    "AP info from path"
    if path == "/":
        return
    ap = getobj(path, AP_FIELDS)
    ssid = ap["Ssid"]
    ap["ssid"] = bytes(ssid).decode() if ssid else None
    if dev:
        ap["dev"] = dev
        ap["ifname"] = nm(dev).Interface
    return ap


@app.route("/nm/accesspoints")
def accesspoints():
    nets = []
    for p in nm().Devices:
        try:
            dev = nm(p)
            if dev.DeviceType == 2:
                nets += [ap(a, p) for a in dev.AccessPoints]
        except:
            pass
    return sorted(nets, key=lambda n: n["Strength"], reverse=True)


@app.route("/nm/ip")
def ip():
    a = nm(request.args.get("path"))
    return {f: getattr(a, f) for f in IP_FIELDS}


@app.route("/nm/up", methods=["POST"])
def up():
    data = request.get_json()
    nm().ActivateConnection(data, "/", "/")
    return {"status": "OK"}


@app.route("/nm/down", methods=["POST"])
def down():
    data = request.get_json()
    if "connection" in data:
        nm().DeactivateConnection(data["connection"])
    if "device" in data:
        nm(data["device"]).Disconnect()
    return {"status": "OK"}


@app.route("/nm/enable", methods=["POST"])
def enable():
    data = request.get_json()
    for k, v in data.items():
        setattr(nm(), k, v)
    return {"status": "OK"}


@app.route("/nm/delete", methods=["POST"])
def delete():
    data = request.get_json()
    nm(data).Delete()
    return {"status": "OK"}


@app.route("/nm/connect", methods=["POST"])
def connect():
    data = request.get_json()
    # print(data)
    psk = data.get("psk")
    if psk:
        con = {"802-11-wireless-security": {"psk": Variant("s", data["psk"])}}
    else:
        con = {}
    nm().AddAndActivateConnection(con, data["dev"], data["path"])
    return {"status": "OK"}


def settings(path, secrets=False) -> Dict[str, Dict[str, Any]]:
    "connection settings from path"
    con = nm(path)
    sets = con.GetSettings()
    if secrets:
        try:
            sec = con.GetSecrets("802-11-wireless-security")
            sets["802-11-wireless-security"].update(sec["802-11-wireless-security"])
        except:
            pass
    return sets


@app.route("/nm/connection")
def connection():
    return settings(request.args.get("path"), True)


VTYPES = {
    "ssid": "ay",
    "proto": "as",
    "group": "as",
    "pairwise": "as",
    "address-data": "aa{sv}",
}


def vtype(k, v):
    t = VTYPES.get(k)
    if t:
        return t
    if isinstance(v, bool):
        return "b"
    if isinstance(v, int):
        return "i"
    return "s"


def toVariant(data):
    var = {}
    for g, s in data.items():
        sub = {}
        var[g] = sub
        for k, v in s.items():
            t = vtype(k, v)
            if k == "ssid":
                v = v.encode()
            if k in ("proto", "group", "pairwise"):
                v = v.split(",")
            if k == "address-data":
                w = []
                for a in v.split(","):
                    a = a.strip().split("/")
                    a = {
                        "address": Variant("s", a[0]),
                        "prefix": Variant("i", int(a[1])),
                    }
                    w.append(a)
                v = w
            print(g, k, t, v)
            sub[k] = Variant(t, v)
    return var


@app.route("/nm/update", methods=["POST"])
def update():
    data = request.get_json()
    print(data)
    uuid = data["connection"].get("uuid")
    data = toVariant(data)
    if uuid:
        path = nm("Settings").GetConnectionByUuid(uuid)
        nm(path).Update(data)
    else:
        nm("Settings").AddConnection(data)
    return {"status": "OK"}


if __name__ == "__main__":
    app.run(debug=True, port=5005)
