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

    def _load_plugins(self):
        sys.path.insert(0, self._plugin_directory)
        for i in os.listdir(self._plugin_directory):
            filename, ext = os.path.splitext(i)
            if ext == '.py':
                print "Loading File: " + filename
                mod = __import__(filename)
                if mod.Plugin():
                    print "Plugin loaded: " + filename
                    HoneypotBase._start_manager_thread(self, mod.Plugin())
        sys.path.pop(0)

    def _start_manager_thread(self, plugin):
        thread = PluginManager(plugin, self._Session)
        thread.start()
        self._threads.append(thread)

    # listens for user commands
    @staticmethod
    def start_interface():
        print("waiting for command")
        while True:
            command = raw_input()
            if command == "start honeypot":
                HoneypotBase()._load_plugins()
            elif command == "stop honeypot":
                HoneypotBase()._stop_hp()
            elif command == "start server":
                HoneypotBase()._start_server()
            elif command == "stop server":
                HoneypotBase()._stop_server()
            elif command == "start all":
                HoneypotBase()._load_plugins()
                HoneypotBase()._start_server()
            elif command == "stop all":
                HoneypotBase()._stop_server()
                HoneypotBase()._stop_hp()
            elif command == "help":
                print ("start honeypot")
                print ("stop honeypot")
                print ("start server")
                print ("stop server")
                print ("start all")
                print ("stop all")
            else:
                print("command not found")

    def _stop_hp(self):
        for thread in self._threads:
            thread.stop()
        raise SystemExit(0)

    def _start_server(self):
        pass

    def _stop_server(self):
        pass

HoneypotBase().start_interface()
