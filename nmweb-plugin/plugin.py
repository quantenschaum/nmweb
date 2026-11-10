import os
import sys
from threading import Thread
from time import sleep
from wsgiref.simple_server import make_server

try:
    from avnav_nmea import NMEAParser
    from avnav_worker import AVNWorker
    from avnrouter import AVNRouter
except:
    pass

sys.path.insert(0, os.path.dirname(__file__))


PLUGIN_VERSION = 20261110
MIN_AVNAV_VERSION = 20261102
PORT = "port"
CONFIG = [
    {
        "name": PORT,
        "description": "nmweb port",
        "type": "NUMBER",
        "default": 8123,
    },
]


class Plugin(object):
    @classmethod
    def pluginInfo(cls):
        return {
            "description": "webinterface to network manager",
            "version": PLUGIN_VERSION,
            "config": CONFIG,
        }

    def __init__(self, api):
        self.api = api
        assert MIN_AVNAV_VERSION <= self.api.getAvNavVersion(), (
            "incompatible AvNav version"
        )
        self.api.registerEditableParameters(CONFIG, self.changeParam)
        self.api.registerRestart(self.stop)
        self.server = None
        self.saveAllConfig()

    def stop(self):
        if self.server:
            self.server.stop()

    def getConfigValue(self, name):
        defaults = self.pluginInfo()["config"]
        for cf in defaults:
            if cf["name"] == name:
                return self.api.getConfigValue(name, cf.get("default"))
        return self.api.getConfigValue(name)

    def saveAllConfig(self):
        d = {}
        defaults = self.pluginInfo()["config"]
        for cf in defaults:
            v = self.getConfigValue(cf.get("name"))
            d.update({cf.get("name"): v})
        self.api.saveConfigValues(d)

    def changeConfig(self, newValues):
        self.api.saveConfigValues(newValues)

    def changeParam(self, param):
        self.api.saveConfigValues(param)
        self.read_config()

    def read_config(self):
        config = {}
        for c in CONFIG:
            name = c["name"]
            TYPES = {"FLOAT": float, "NUMBER": int, "BOOLEAN": lambda s: s == "True"}
            value = self.getConfigValue(name)
            value = TYPES.get(c.get("type"), str)(value)
            config[name] = value
        # print("config", config)
        self.config = config

    def run(self):
        self.api.setStatus("STARTED", "starting")
        while not self.api.shouldStopMainThread():
            try:
                self.read_config()
                url = f"http://$HOST:{self.config[PORT]}/"
                self.api.registerUserApp(
                    url,
                    "dist/nm.png",
                    shortText="nmweb",
                    longText="network manager",
                    page="serverpage",
                    name="ui",
                )

                from nmweb import app

                self.server = Server(app, port=self.config[PORT])
                self.api.setStatus("NMEA", f"running at {url}")
                self.server.start()

            except Exception as x:
                self.api.error(f"{x}")
                self.api.setStatus("ERROR", f"{x}")
                sleep(10)
            finally:
                self.stop()


class Server:
    def __init__(self, app, host="0.0.0.0", port=8080):
        self.httpd = make_server(host, port, app)

    def start(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
