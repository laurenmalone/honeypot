import sqlite3

class HoneypotBase:

    # db = 'sqliteDB/test.db'
    db_location = None
    plugin_directory = None
    threads = []




    # call start_manager_thread() for each item in plugins
    @staticmethod
    def load_plugins(directory):
        pass

    def start_manager_thread(db_location, plugin):
        pass

    # listens for user commands
    @staticmethod
    def start_interface():
        pass

    # kill program - kill manager threads.
    @staticmethod
    def stop():
        pass

#__all__ = ["load_plugins", "start_manager_thread", "stop", "start_interface", "threads"]