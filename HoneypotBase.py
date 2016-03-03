from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PluginManager import PluginManager
import os
import sys


class HoneypotBase:
    def __init__(self):
        self._plugin_directory = './plugins/'
        self._threads = []
        self._engine = create_engine('sqlite:///sqliteDB/test.db', echo=True)
        self._Session = sessionmaker(bind=self._engine)

    def load_plugins(self):
        sys.path.insert(0, self._plugin_directory)
        for i in os.listdir(self._plugin_directory):
            filename, ext = os.path.splitext(i)
            if ext == '.py':
                print "Loading File: " + filename
                try:
                    mod = __import__(filename)
                    HoneypotBase._start_manager_thread(self, mod.Plugin())
                    print "Plugin loaded: " + filename
                except AttributeError:
                    print("Invalid plugin: " + filename)
                except IndentationError:
                    print("Plugin in wrong format: " + filename)
        sys.path.pop(0)

    def _start_manager_thread(self, plugin):
        thread = PluginManager(plugin, self._Session)
        thread.start()
        self._threads.append(thread)

HoneypotBase().load_plugins()
