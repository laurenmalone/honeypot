from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError, OperationalError
from sqlalchemy import *
from PluginManager import PluginManager
import os
import sys
import logging
import datetime
import signal
from base import Base
from ConfigParser import SafeConfigParser
import ast

_threads = []
_plugin_list = []
_catch_all_list = []


my_date_time = datetime.datetime

_plugin_directory = null
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
    Get list of ports to listen on.
    """
    global _db, _plugin_directory, log, _engine, _Session, _catch_all_list
    parser = SafeConfigParser()
    parser.read(_config)

    _db = parser.get('honeypot', 'db')
    _plugin_directory = parser.get('honeypot', 'plugins')
    log = parser.get('honeypot', 'log')

    _engine = create_engine(_db, echo=False)
    _Session.configure(bind=_engine)

    logging.basicConfig(filename=log, level=logging.DEBUG)
    _catch_all_list = ast.literal_eval(parser.get('honeypot', 'ports'))
    print _catch_all_list


def _import_plugins():
    try:
        sys.path.insert(0, _plugin_directory)
        os.listdir(_plugin_directory)

    except OSError:
        print("Plugin folder not found.")
        return

    else:
        for i in os.listdir(_plugin_directory):
            filename, ext = os.path.splitext(i)

            if filename == '__init__' or ext != '.py' or filename == 'dummy_plugin':
                continue

            try:
                mod = __import__(filename)
                plugin = mod.Plugin()
                port = plugin.get_port()
                if port in _catch_all_list:
                    _catch_all_list.remove(port)
                    add_item_to_table(plugin)
                    add_item_to_plugin_list(plugin)

            except:
                logging.exception(filename + " cannot be loaded " ":Time: " + str(my_date_time.now()))

        sys.path.pop(0)


def add_item_to_plugin_list(plugin):
    port = plugin.get_port()
    if _port_valid(port):
        if port == 0:  # add to end of list
            _plugin_list.append(plugin)

        else:
            _plugin_list.insert(0, plugin)  # add to beginning of list
        print plugin.get_display() + " successfully loaded " + str(plugin.get_port())
        return True

    else:
        logging.exception(plugin.get_value() + " not loaded, port already in use :Time: " + str(my_date_time.now()))
        return False


def _start_catchall_plugins():
    print _catch_all_list
    if len(_catch_all_list) < 0:
        return False

    import plugins.dummy_plugin
    add_item_to_table(plugins.dummy_plugin.Plugin())
    for i in range(len(_catch_all_list)):
        dummy = plugins.dummy_plugin.Plugin()
        port = _catch_all_list[i]
        dummy.set_port(port)
        add_item_to_plugin_list(dummy)
        return True


def add_item_to_table(plugin):
    try:
        session = _Session()
        q = session.query(Plugin.id).filter(Plugin.display == plugin.get_display())
        if q.count() > 0:
            return

        record = Plugin(display=plugin.get_display(), description=plugin.get_description(),
                        orm=str(plugin.get_orm()), value=(plugin.get_value()))
        session.add(record)
        session.commit()
        session.close()
        #print plugin.get_display() + " added to plugin table"
        return True

    except:
        logging.exception(plugin.get_value + " could not be added to plugins table :Time: " + str(my_date_time.now()))
        return False

def _port_valid(port):
    """Check that given port is valid and available.

    param: port -- the port being checked
    return: True if port is valid and available, False otherwise
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
    except:
        logging.exception("plugin table not created " ":Time: " + str(my_date_time.now()))



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
    _create_plugin_tables()
    _import_plugins()
    _start_catchall_plugins()
    _start_manager_threads()

    #wait for program to be killed
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.pause()


if __name__ == "__main__":
    run()

