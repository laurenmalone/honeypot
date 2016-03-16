import socket
from threading import Thread, Event

class PluginManager(Thread):
    """Listens for incoming connections on behalf of a plugin.

    When a new connection is made, it's handed off to the plugin along
    with a database session, and the PluginManager goes back to listen
    for more connections.
    """

    def __init__(self, plugin, session_factory):
        """Accepts a plugin and a session factory.

        The sessions created by the factory are used by the plugin to
        talk with the database.
        """
        Thread.__init__(self)
        self._plugin = plugin
        self._session_factory = session_factory
        self._flag = Event()

    def run(self):
        """Listens for incoming connections, hands them off to the plugin.

        Overrides Thread.run().
        """
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('', self._plugin.get_port()))
        serversocket.listen(5)
        while True:
            clientsocket, address = serversocket.accept()
            if self._flag.is_set():
                clientsocket.close()
                break
            else:
                args = clientsocket, address, self._session_factory()
                Thread(target=self._plugin.run, args=args).start()
        serversocket.close()

    def stop(self):
        """Causes run() to stop listening for connections and return."""
        self._flag.set()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self._plugin.get_port()))
        sock.close()

