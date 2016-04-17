from sqlalchemy.orm import sessionmaker
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
import plugins.dummy_plugin

""" Note - this class uses broad exceptions because it doesn't care why any one plugin didn't load,
persist to db, etc. The error is simply logged, and the the show must go on. Specific errors must be
caught by the plugin writer.

"""
thread_list = []            # keep track of plugin manager threads
plugin_instance_list = []   # plugin instances, used to start plugin manager threads
plugin_list = []            # plugins that are successfully imported, used to add records to plugin table
catch_all_list = []         # list of ports user wants to listen on

my_date_time = datetime.datetime

plugin_directory = null
db = null
Session = sessionmaker()
engine = null
config = 'honeypot.ini'


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


def read_config():
    """Initialize settings

    Get locations of db, log, and plugins.
    Create engine and sessionmaker for interacting with db.
    Get list of ports to listen on.
    """
    global db, plugin_directory, log, engine, Session, catch_all_list
    parser = SafeConfigParser()
    parser.read(config)

    db = parser.get('honeypot', 'db')
    plugin_directory = parser.get('honeypot', 'plugins')
    log = parser.get('honeypot', 'log')

    engine = create_engine(db, echo=False)
    Session.configure(bind=engine)
    logging.basicConfig(filename=log, level=logging.DEBUG)
    catch_all_list = ast.literal_eval(parser.get('honeypot', 'ports'))


def import_plugins():
    """Import plugins

    Add successfully imported plugins to plugin_list.
    return: bool -- False if plugin folder cannot be found, True otherwise.
    Raise OSError if plugin directory isn't found.
    Raise exception if a plugin cannot be imported.
    """
    try:
        sys.path.insert(0, plugin_directory)
        os.listdir(plugin_directory)

    except OSError:
        print("Plugin directory not found.")
        return False

    else:
        for i in os.listdir(plugin_directory):
            filename, ext = os.path.splitext(i)

            if filename == '__init__' \
                    or ext != '.py' \
                    or filename == 'dummy_plugin' \
                    or filename == 'plugin_template':
                continue

            try:
                mod = __import__(filename)
                plugin = mod.Plugin()
                port = plugin.get_port()
                if port in catch_all_list:
                    catch_all_list.remove(port)  # so that list only contains ports with unspecified plugins
                    if add_item_to_plugin_instance_list(plugin):
                        plugin_list.append(plugin)

            except:
                logging.exception(filename + " cannot be loaded " ":Time: " + str(my_date_time.now()))
                print (filename + "cannot be loaded")

        sys.path.pop(0)
        return True


def add_item_to_plugin_instance_list(plugin):
    """Add a newly created plugin instance to plugin_instance_list
    (Later used to start plugin managers)

    plugin: item to add
    return: True if item is added, False otherwise
    """
    port = plugin.get_port()
    if port_valid(port):
        plugin_instance_list.append(plugin)
        print plugin.get_display() + " listening on port " + str(plugin.get_port())
        return True

    else:
        logging.exception(plugin.get_value() + " not loaded, port " + str(port)+
                          " already in use :Time: " + str(my_date_time.now()))
        return False


def set_catchall_plugins():
    """Create catchall plugin for every port in catch_all_list

    (At this point in program, catch_all_list only consists of ports without specified plugin)
    Add catchall plugins to plugin_instance_list
    If catchall plugins are created, add dummy_plugin to plugins table
    return: True if catchall plugins are created, False otherwise
    """
    if len(catch_all_list) < 0:
        return False

    add_record_to_plugin_table(plugins.dummy_plugin.Plugin())
    for i in range(len(catch_all_list)):
        dummy = plugins.dummy_plugin.Plugin()
        port = catch_all_list[i]
        dummy.set_port(port)
        add_item_to_plugin_instance_list(dummy)
    return True


def add_records_to_plugin_table():
    """Add record to plugin table for every item in plugin_list
    """
    for i in plugin_list:
        add_record_to_plugin_table(i)


def add_record_to_plugin_table(plugin):
    """Add a single record to plugin table

    param: plugin -- plugin being added to table
    return: True if table has been added or already exists, False otherwise
    Raise exception if record cannot be added
    """
    try:
        session = Session()
        q = session.query(Plugin.id).filter(Plugin.display == plugin.get_display())
        if q.count() > 0:
            return True

        record = Plugin(display=plugin.get_display(), description=plugin.get_description(),
                        orm=str(plugin.get_orm()), value=(plugin.get_value()))
        session.add(record)
        session.commit()
        session.close()
        return True

    except:
        logging.exception(plugin.get_value + " could not be added to plugins table :Time: " + str(my_date_time.now()))
        return False


def port_valid(port):
    """Check that given port is valid and available.

    param: port -- the port being checked
    return: True if port is valid and available, False otherwise
    """
    for i in plugin_instance_list:

        if i.get_port() == port:
            return False

        if port > 65535 or port < 1:
            return False
    return True


def create_tables():
    """Create tables that are defined by plugins

    For each class that inherits from declarative base and defines both __tablename__ and primary key.
    Raise exception if tables are not created successfully.
    Because Python can't "unimport", tables will also be created for plugins that are invalid.
    (since plugin has to be imported to check for validity)
    However, the plugin will not run, it will not have a place in the plugins table, and data will
    not be recorded to its own table.
    """
    try:
        Base.metadata.create_all(engine)
    except:
        logging.exception("plugin table not created " ":Time: " + str(my_date_time.now()))


def start_manager_threads():
    """Start a PluginManager thread for each item in plugin_instance_list
    """
    for plugin in plugin_instance_list:
        thread = PluginManager(plugin, Session)
        thread.start()
        thread_list.append(thread)


def signal_handler(signal, frame):
    """ Stop each PluginManager thread in threads."""
    for thread in thread_list:
        thread.stop()
        thread.join()


def run():
    """ Drive program."""
    read_config()
    if not import_plugins():
        raise SystemExit(1)  # no point in going on
    create_tables()
    add_records_to_plugin_table()
    set_catchall_plugins()
    start_manager_threads()

    # wait for program to be killed
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()


if __name__ == "__main__":
    run()
