#!/usr/bin/python3

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

objpath = "/runner" # Default value for X-Plasma-DBusRunner-Path metadata property
iface = "org.kde.krunner1"


class Runner(dbus.service.Object):
    def __init__(self):
        self.session_bus = dbus.SessionBus()
        dbus.service.Object.__init__(self, dbus.service.BusName("org.kde.KrunnerSpotify", dbus.SessionBus()), objpath)

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        if query == "pause" or query == "playpause":
            # data, text, icon, type (KRunner::QueryType), relevance (0-1), properties (subtext, category, multiline(bool) and urls)
            return [("playpause", "Pause Spotify playback", "document-edit", 100, 1.0, {})]
        elif query == "next" or query == "skip":
            return [("next", "Play next song", "document-edit", 100, 1.0, {})]
        elif query == "prev" or query == "previous":
            return [("prev", "Play previous song", "document-edit", 100, 1.0, {})]
        return []

    @dbus.service.method(iface, out_signature='a(sss)')
    def Actions(self):
        # id, text, icon
        return [("id", "playpause", "planetkde")]

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, data: str, action_id: str):
        try:
            spotify_proxy = self.session_bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        except:
            return
        if data == "playpause":
            spotify_proxy.get_dbus_method("PlayPause", "org.mpris.MediaPlayer2.Player")()
        elif data == "next":
            spotify_proxy.get_dbus_method("Next", "org.mpris.MediaPlayer2.Player")()
        elif data == "prev":
            spotify_proxy.get_dbus_method("Previous", "org.mpris.MediaPlayer2.Player")()

runner = Runner()
loop = GLib.MainLoop()
loop.run()
