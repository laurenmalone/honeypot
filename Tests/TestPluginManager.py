import socket
import time
from unittest import TestCase
from PluginManager import PluginManager

class TestPluginManager(TestCase):
    def test_stop(self):
        class Plugin:
            def __init__(self):
                sock = socket.socket()
                sock.bind(('', 0)) # bind to any available port
                self._port = sock.getsockname()[1]
                sock.close()
            def get_port(self):
                return self._port
        plugin_manager = PluginManager(Plugin(), lambda: None)
        plugin_manager.start()
        time.sleep(1)
        plugin_manager.stop()
        plugin_manager.join()
        self.assertFalse(plugin_manager.is_alive())

