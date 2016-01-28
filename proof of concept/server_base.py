import os
import sys
import socket

path = "plugins/"
plugins = {}
HOST = ''
ports = []

sys.path.insert(0, path)
for i in os.listdir(path):
    fname, ext = os.path.splitext(i)
    if ext == '.py':
        mod = __import__(fname)
        if mod.Plugin():
            plugins[fname] = mod.Plugin()
            print "Plugin loaded: " + fname
            plugin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = plugins[fname].get_port()
            print "Opening Socket for " + fname + " on Port: " + str(port)
            plugin_socket.bind((HOST, int(port)))
            ports.append(port)
            plugins[fname].run(plugin_socket)
sys.path.pop(0)

#for plugin in plugins.values():
 #   plugin.run()

