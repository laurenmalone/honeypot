from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PluginManager import PluginManager
import os
import datetime
import sys

my_date_time = datetime.datetime
plugins = {}


class HoneypotBase:
    def __init__(self):
        self._plugin_directory = "./proof_of_concept/plugins/"
        self._threads = []
        self.engine = create_engine('sqlite:///sqliteDB/test.db', echo=True)
        self.Session = sessionmaker(bind=self.engine)

    # call start_manager_thread() for each item in plugins
    def load_plugins(self):

        sys.path.insert(0, self._plugin_directory)
        for i in os.listdir(self._plugin_directory):
            filename, ext = os.path.splitext(i)
            if ext == '.py':
                print "Loading File: " + filename
                mod = __import__(filename)
                if mod.Plugin():
                    plugins[filename] = mod.Plugin()
                print "Plugin loaded: " + filename
                HoneypotBase.start_manager_thread(self,mod.Plugin())

    def start_manager_thread(self, plugin):
        thread = PluginManager(plugin, self.Session)
        thread.start()
        self._threads.append(thread)

    # listens for user commands
    @staticmethod
    def start_interface():
        while True:
            print("waiting for command")
            command = raw_input()
            if command == "start honeypot":
                HoneypotBase().load_plugins()
            elif command == "stop honeypot":
                HoneypotBase().stop_hp()
            elif command == "start server":
                HoneypotBase().start_server()
            elif command == "stop server":
                HoneypotBase().stop_server()
            elif command == "start all":
                sys.path.insert(0, HoneypotBase()._plugin_directory)
                HoneypotBase().load_plugins()
                HoneypotBase().start_server()
            elif command == "help":
                pass
            else:
                print("command not found\n")

    # kill program - kill manager threads
    def stop_hp(self):
        for thread in self._threads:
            thread.stop()
        raise SystemExit(0)

    def start_server(self):
        pass

    def stop_server(self):
        sys.path.pop(0)
        pass


HoneypotBase().start_interface()
