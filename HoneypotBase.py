from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class HoneypotBase:


    plugin_directory = None
    threads = []

    engine = create_engine('sqlite:///sqliteDB/test.db', echo=True)
    Session = sessionmaker(bind=engine)

    # call start_manager_thread() for each item in plugins
    @staticmethod
    def load_plugins(directory):
        pass

    @classmethod
    def start_manager_thread(self, plugin):
        thread = PluginManager()
        thread.start(plugin, self.Session)


    # listens for user commands
    @staticmethod
    def start_interface():
        pass

    # kill program - kill manager threads.
    @staticmethod
    def stop():
        pass
