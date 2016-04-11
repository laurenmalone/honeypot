import socket
import time
from threading import Event
from unittest import TestCase
from honeypot.PluginManager import PluginManager

class TestPluginManager(TestCase):

    def test_stop(self):
        """Test connecting to plugin's port, stopping PluginManager."""

        class Plugin:
            """Mock plugin, uses random available port."""

            def __init__(self):
                sock = socket.socket()
                sock.bind(('', 0)) # bind to any available port
                self._port = sock.getsockname()[1]
                sock.close()
                self.run_called = Event()

            def get_port(self):
                return self._port

            def run(self, sock, address, session):
                self.run_called.set()

        plugin = Plugin()
        plugin_manager = PluginManager(plugin, lambda: None)
        plugin_manager.start()
        time.sleep(0.01)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', plugin.get_port()))
        sock.close()
        time.sleep(0.01)
        self.assertTrue(plugin.run_called.is_set())
        plugin_manager.stop()
        plugin_manager.join()
        self.assertFalse(plugin_manager.is_alive())

