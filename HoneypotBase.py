from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from PluginManager import PluginManager
import os
import sys
import logging
import datetime
import signal


engine = create_engine('sqlite:///test.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

plugin_directory = 'plugins/'
threads = []
plugin_list = []

my_date_time = datetime.datetime
logging.basicConfig(filename='honey.log', level=logging.DEBUG)


class Plugin(Base):
        __tablename__ = 'plugin'

        id = Column(Integer, Sequence('plugin_id_seq'), primary_key=True, nullable=False)
        name = Column(String,nullable=False )
        orm = Column(String, nullable=False)
        description = Column(String, nullable=False)


def _load_plugins():
    try:
        sys.path.insert(0, plugin_directory)
        os.listdir(plugin_directory)

    except OSError:
        print("Plugin folder not found.")
        print(sys.path)
        raise SystemExit(1)

    else:
        for i in os.listdir(plugin_directory):
            filename, ext = os.path.splitext(i)
            if filename == '__init__' or ext != '.py':
                continue
            print filename + ext+ " loading..."
            try:
                mod = __import__(filename)
                plugin = mod.Plugin()
                if _port_already_used(plugin):
                    logging.exception(filename + " not loaded :Time: " + str(my_date_time.now()))
                    print (filename + " not loaded. Port " + plugin.get_port+ " already in use.")
                else:
                    plugin_list.append(plugin)
                    print (filename + ext + " successfuly loaded")
            except Exception:
                logging.exception(filename + " not loaded " ":Time: " + str(my_date_time.now()))
                print (filename + ext + " not loaded")
        sys.path.pop(0)


def _port_already_used(plugin):
    for i in plugin_list:
        if i.get_port() == plugin.get_port():
            return True
    return False


def _start_manager_threads():
    # start a plugin manager thread for each plugin
    for plugin in plugin_list:
        thread = PluginManager(plugin, Session)
        thread.start()
        threads.append(thread)


def _signal_handler(signal, frame):
    # called on ctrl c or kill pid
    print(signal)
    for thread in threads:
        thread.stop()
    print 'Exiting honeypot'


def _add_plugin_table():
    # add plugin table to db
    session = Session()
    #for i in plugins:
        #record = Plugin(name = i.)
        #session.add(record)
    #session.commit()
    session.close()


def _create_plugin_tables():
    # add table to db for each plugin

    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        print"Db directory doesn't exist."
        raise SystemExit(1)


def run():

    _load_plugins()

    _add_plugin_table()

    _create_plugin_tables()

    _start_manager_threads()

    # wait for program to be killed
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.pause()


if __name__ == "__main__":
    run()