#!/usr/bin/env python
import sys, time, re
import dbus, dbus.glib, gobject
from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record as CouchRecord

COUCH_MESSAGE_TYPE = "http://none/couch/message"
URL_REGEX = re.compile("(?<!\w)((?:http|https|ftp|mailto):/*(?!/)(?:[\w$\+\*@&=\-/]|%[a-fA-F0-9]{2}|[\?\.:\(\),;!'\~](?!(?:\s|$))|(?:(?<=[^/:]{2})#)){2,})")

XCHAT_PLUGIN_FILE = sys.argv[0]
XCHAT_PLUGIN_NAME = "LinkCollector"
XCHAT_PLUGIN_DESC = "Collects links from XChat messages"
XCHAT_PLUGIN_VER = "1.0"

database = CouchDatabase("links", create=True)
bus = dbus.SessionBus()

purple_obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(purple_obj, "im.pidgin.purple.PurpleInterface")


def on_purple_message(account, name, message, conv, flags):
  for url in URL_REGEX.findall(message):
    record = CouchRecord({
      "program": "pidgin",
      "message": message,
      "time": time.time(),
      "user": name,
      "url": url,
    }, COUCH_MESSAGE_TYPE)
    database.put_record(record)

bus.add_signal_receiver(on_purple_message,
    "ReceivedImMsg", "im.pidgin.purple.PurpleInterface")

gobject.MainLoop().run()
