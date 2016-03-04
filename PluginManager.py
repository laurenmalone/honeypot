import socket
from threading import Thread, Event

class PluginManager(Thread):
    def __init__(self, plugin, session_factory):
        Thread.__init__(self)
        self._plugin = plugin
        self._session_factory = session_factory
        self._flag = Event()

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('', self._plugin.get_port()))
        serversocket.listen(5)
        while 1:
            clientsocket, address = serversocket.accept()
            if self._flag.is_set():
                clientsocket.close()
                break
            else:
                args = clientsocket, address, session_factory()
                Thread(target = self._plugin.run, args = args).start()
        serversocket.close()

    def stop(self):
        self._flag.set()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self._plugin.get_port()))
        sock.close()

