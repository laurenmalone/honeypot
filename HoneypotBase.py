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

thread_list = []
plugin_instance_list = []
plugin_list = []
catch_all_list = []


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
    #print catch_all_list


def import_plugins():
    try:
        sys.path.insert(0, plugin_directory)
        os.listdir(plugin_directory)

    except OSError:
        print("Plugin folder not found.")
        return

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
                    catch_all_list.remove(port)
                    #plugin_list.append(plugin)
                    if add_item_to_plugin_instance_list(plugin):
                        plugin_list.append(plugin)

            except:
                logging.exception(filename + " cannot be loaded " ":Time: " + str(my_date_time.now()))

        sys.path.pop(0)


def add_item_to_plugin_instance_list(plugin):
    port = plugin.get_port()
    if port_valid(port):
        plugin_instance_list.append(plugin)
        print plugin.get_display() + " listening on port " + str(plugin.get_port())
        return True

    else:
        logging.exception(plugin.get_value() + " not loaded, port already in use :Time: " + str(my_date_time.now()))
        return False


def start_catchall_plugins():
    #print catch_all_list
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
    for i in plugin_list:
        add_record_to_plugin_table(i)


def add_record_to_plugin_table(plugin):
    try:
        session = Session()
        q = session.query(Plugin.id).filter(Plugin.display == plugin.get_display())
        if q.count() > 0:
            return

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
    """Create tables that are defined by plugins.

    For each class that inherits from declarative base and defines __tablename__.
    Raise SQLAlchemyError if a table is not created successfully.
    """
    try:
        Base.metadata.create_all(engine)
    except:
        logging.exception("plugin table not created " ":Time: " + str(my_date_time.now()))


def start_manager_threads():
    """Start a PluginManager thread for each item in plugins
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
    import_plugins()
    create_tables()
    add_records_to_plugin_table()
    start_catchall_plugins()
    start_manager_threads()

    #wait for program to be killed
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()


if __name__ == "__main__":
    run()
