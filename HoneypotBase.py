from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from sqlalchemy import *
from PluginManager import PluginManager
import os
import sys
import logging
import datetime
import signal
import traceback
from base import Base
from ConfigParser import SafeConfigParser

_threads = []
_plugin_list = []
my_date_time = datetime.datetime

_plugins = null
_db = null
_Session = sessionmaker()
_engine = null
_config = 'honeypot.ini'


class Plugin(Base):
    """Represent plugin table in db.

    Inherit declarative base class from base.py
    """
    __tablename__ = 'plugin'
    id = Column(Integer, primary_key=True)
    display = Column(String, nullable=False)
    description = Column(String, nullable=False)
    orm = Column(String, nullable=False)
    value = Column(String, nullable=False)


def _read_config():
    """Initialize settings

    Get locations of db, log, and plugins.
    Create engine and sessionmaker for interacting with db.
    """
    global _db, _plugins, log, _engine, _Session
    parser = SafeConfigParser()
    parser.read(_config)

    _db = parser.get('honeypot', 'db')
    _plugins = parser.get('honeypot', 'plugins')
    log = parser.get('honeypot', 'log')

    _engine = create_engine(_db, echo=False)
    _Session.configure(bind=_engine)

    logging.basicConfig(filename=log, level=logging.DEBUG)


def _import_plugins():
    """Import plugins.

    Add successfully imported plugins to plugin_list.
    return: bool -- False if plugin folder cannot be found, True otherwise.
    Raise OSError if plugin folder isn't found.
    Raise Exception if a plugin cannot be imported.
    """
    try:
        sys.path.insert(0, _plugins)
        os.listdir(_plugins)

    except OSError:
        print("Plugin folder not found.")
        return False

    else:
        for i in os.listdir(_plugins):
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
                    if plugin.get_port == 0:  # add to end of list
                        _plugin_list.append(plugin)

                    else:
                        _plugin_list.insert(0, plugin)  # add to beginning of list

                    print (filename + ext + " successfully loaded")

            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print(e)
                logging.exception(filename + " not loaded " ":Time: " + str(my_date_time.now()))
                print (filename + ext + " not loaded")

        sys.path.pop(0)
        return True


def _port_valid(port):
    """Check that given port is valid and available.

    param: port -- the port being checked
    return: bool -- True if port is valid and available, False otherwise
    """
    for i in _plugin_list:

        if i.get_port() == port and port != 0:
            return False

        if port > 65535:
            return False
    return True


def _create_plugin_tables():
    """Create tables that are defined by plugins.

    For each class that inherits from declarative base and defines __tablename__.
    Raise SQLAlchemyError if a table is not created successfully.
    """
    try:
        Base.metadata.create_all(_engine)
    except InvalidRequestError as e:
        print(e)
    except Exception as e:
        #print(e)
        logging.exception("plugin table not created " ":Time: " + str(my_date_time.now()))


def _add_items_to_plugin_table():
    """Insert an item into plugin table for each item in plugins_list.

    Raise AttributeError if a plugin does not have attributes required for visual tool.
    Raise SQLAlchemyError if an item is not added to plugin table successfully.
    """
    session = _Session()
    for i in _plugin_list:

        try:
            q = session.query(Plugin).filter(Plugin.display == i.get_display())
            if q.count() > 0:
                continue
            record = Plugin(display=i.get_display(), description=i.get_description(),
                            orm=str(i.get_orm()), value=(i.get_value()))
        except AttributeError:
            print "Plugin does not have attributes to use visual tool"
            logging.exception("Plugin does not have attributes to use visual tool :Time: " + str(my_date_time.now()))
        else:
            try:
                session.add(record)
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                logging.exception("record not added to table " ":Time: " + str(my_date_time.now()))

    session.close()


def _start_manager_threads():
    """Start a PluginManager thread for each item in plugins
    """
    for plugin in _plugin_list:
        thread = PluginManager(plugin, _Session)
        thread.start()
        _threads.append(thread)


def _signal_handler(signal, frame):
    """ Stop each PluginManager thread in threads."""
    for thread in _threads:
        thread.stop()
        thread.join()


def run():
    """ Drive program."""
    _read_config()

    if not _import_plugins():
        raise SystemExit(1)

    _create_plugin_tables()

    _add_items_to_plugin_table()

    _start_manager_threads()

    # wait for program to be killed
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.pause()


if __name__ == "__main__":
    run()

