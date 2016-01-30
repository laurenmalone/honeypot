import os
import sys
import socket
import logging
import sqlite3
import datetime

my_date_time = datetime.datetime
logging.basicConfig(filename='honey.log', level=logging.DEBUG)

print "Honey Pot Starting...."
logging.info("Honey Pot Started: " + str(my_date_time.now()))
status = "Running"

conn = sqlite3.connect('sqliteDB/test.db')
print "test.db opened"
logging.info("test.db opened: " + str(my_date_time.now()))

path = "plugins/"
plugins = {}
HOST = ''
ports = []


def setup_db_table(orm):
    logging.info("Creating Table: " + orm['table']['tableName'] + ":Time: " + str(my_date_time.now()))
    statement = 'CREATE TABLE ' + orm['table']['tableName'] + '(ID INT PRIMARY KEY NOT NULL,'
    for item in orm['table']:
        if not item == "tableName":
            print orm['table'][item]['name']
            statement += orm['table'][item]['name'] + " " + orm['table'][item]['type']
    statement += ');'
    conn.execute(statement)


def load_plugins():
    for i in os.listdir(path):
        fname, ext = os.path.splitext(i)
        if ext == '.py':
            print "Loading File: " + fname
            logging.info("Loading File: " + fname + ":Time: " + str(my_date_time.now()))
            mod = __import__(fname)
            if mod.Plugin():
                plugins[fname] = mod.Plugin()

                print "Plugin loaded: " + fname
                logging.info("Plugin loaded: " + fname + ":Time: " + str(my_date_time.now()))

                plugin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port = plugins[fname].get_port()
                setup_db_table(plugins[fname].get_orm())
                print "Opening Socket for " + fname + " on Port: " + str(port)
                logging.info("Plugin loaded: " + fname + ":Time: " + str(my_date_time.now()))

                plugin_socket.bind((HOST, int(port)))
                ports.append(port)
                plugins[fname].run(plugin_socket)


sys.path.insert(0, path)
load_plugins()
sys.path.pop(0)



#for plugin in plugins.values():
 #   plugin.run()



