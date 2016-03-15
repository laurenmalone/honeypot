from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import *
from PluginManager import PluginManager
import os
import sys
import logging
import datetime
import signal
import traceback
from base import Base


engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(bind=engine)

plugin_directory = 'plugins/'
threads = []
plugin_list = []

my_date_time = datetime.datetime
logging.basicConfig(filename='honey.log', level=logging.DEBUG)


class Plugin(Base):

        __tablename__ = 'plugin'
        id = Column(Integer, primary_key=True)
        display = Column(String, nullable=False)
        description = Column(String, nullable=False)
        orm = Column(String, nullable=False)


def _load_plugins():

    try:
        sys.path.insert(0, plugin_directory)
        os.listdir(plugin_directory)

    except OSError:
        print("Plugin folder not found.")
        return False

    else:
        for i in os.listdir(plugin_directory):
            filename, ext = os.path.splitext(i)
            if filename == '__init__' or ext != '.py':
                continue
            print filename + ext+ " loading..."

            try:
                mod = __import__(filename)
                plugin = mod.Plugin()
                if not _port_valid(plugin.get_port()):
                    logging.exception(filename + " not loaded :Time: " + str(my_date_time.now()))
                    print (filename + " not loaded. Port " + str(plugin.get_port()) + " not available.")

                else:
                    if plugin.get_port == 0: # add to end of list
                        plugin_list.append(plugin)

                    else:
                        plugin_list.insert(0, plugin)

                    print (filename + ext + " successfuly loaded")

            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print(e)
                logging.exception(filename + " not loaded " ":Time: " + str(my_date_time.now()))
                print (filename + ext + " not loaded")

        sys.path.pop(0)
        return True


def _port_valid(port):

    for i in plugin_list:

        if i.get_port() == port and port != 0:
            return False

        if port > 65535:
            return False
    return True


def _start_manager_threads():
    # start a plugin manager thread for each plugin

    for plugin in plugin_list:
        thread = PluginManager(plugin, Session)
        thread.start()
        threads.append(thread)


def _signal_handler(signal, frame):
    # called on ctrl c or kill pid

    for thread in threads:
        thread.stop()
        thread.join()


def _add_plugin_table():
    # add plugin table to db

    session = Session()
    for i in plugin_list:
        try:
            record = Plugin(display=i.get_display(), description=i.get_description(), orm=str(i.get_orm()))
        except AttributeError:
            print "Plugin does not have attributes to use visual tool"
        else:
            try:
                session.add(record)
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                logging.exception("record not added to table " ":Time: " + str(my_date_time.now()))
                return False

    session.close()
    return True


def _create_plugin_tables():
    # add table to db for each plugin

    try:
        Base.metadata.create_all(engine)
        return True

    except SQLAlchemyError as e:
        print(e)
        logging.exception("plugin table not created " ":Time: " + str(my_date_time.now()))
        return False


def run():

    if not _load_plugins():
        raise SystemExit(1)

    _create_plugin_tables()

    _add_plugin_table()

    _start_manager_threads()

    # wait for program to be killed
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.pause()


if __name__ == "__main__":
    run()

