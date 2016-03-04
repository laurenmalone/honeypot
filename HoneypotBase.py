from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from PluginManager import PluginManager
import os
import sys


def _load_plugins():
    sys.path.insert(0, plugin_directory)
    for i in os.listdir(plugin_directory):
        filename, ext = os.path.splitext(i)
        if ext == '.py':
            print "Loading File: " + filename
            try:
                mod = __import__(filename)
                _start_manager_thread(mod.Plugin())
                plugins.append(mod.Plugin)
                print "Plugin loaded: " + filename
            except AttributeError:
                print("Invalid plugin: " + filename)
            except IndentationError:
                print("Plugin in wrong format: " + filename)
    sys.path.pop(0)


def _start_manager_thread(plugin):
    thread = PluginManager(plugin, Session)
    thread.start()
    threads.append(thread)


def _stop_hp():
    for thread in threads:
        thread.stop()
    raise SystemExit(0)


def start():
    try:
        _load_plugins()
        while True:
            continue
    except KeyboardInterrupt:
        _stop_hp()


plugin_directory = './plugins/'
threads = []
plugins = []
engine = create_engine('sqlite:///sqliteDB/test.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
start()
