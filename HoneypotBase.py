from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from PluginManager import PluginManager
import os
import sys
import time
import logging
import datetime


def _load_plugins():
    try:
        sys.path.insert(0, plugin_directory)
        for i in os.listdir(plugin_directory):
            filename, ext = os.path.splitext(i)
            if filename == '__init__':
                continue
            if ext == '.py':
                print "Loading File: " + filename
                try:
                    mod = __import__(filename)
                    plugin = mod.Plugin
                    if _port_already_open(plugin):
                        print (filename + " not loaded. Port already in use.")
                    else:
                        plugins.append(plugin)
                    print ("Plugin loaded: " + filename)
                except AttributeError:
                    print("Invalid plugin: " + filename)
                except IndentationError:
                    print("Plugin in wrong format: " + filename)
        sys.path.pop(0)
    except OSError:
        print("Plugin folder not found.")
        raise SystemExit(1)


def _port_already_open(plugin):
    for i in plugins:
        if i.get_port() == plugin.get_port():
            return True
    return False


def _start_manager_threads():
    for plugin in plugins:
        thread = PluginManager(plugin, Session)
        thread.start()
        threads.append(thread)


def _stop_hp():
    for thread in threads:
        thread.stop()
    raise SystemExit(0)


def _wait():
    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        _stop_hp()


plugin_directory = './plugins/'
threads = []
plugins = []

my_date_time = datetime.datetime
logging.basicConfig(filename='honey.log', level=logging.DEBUG)

try:
    engine = create_engine('sqlite:///test.db', echo=True)
    Base = declarative_base()
    _load_plugins()
    Base.metadata.create_all(engine)

except OperationalError:
    print"Db directory doesn't exist."
    raise SystemExit(1)

Session = sessionmaker(bind=engine)
_start_manager_threads()
_wait()
