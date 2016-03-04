import time
from unittest import TestCase
from PluginManager import PluginManager

class TestPluginManager(TestCase):
    def test_stop(self):
        class Plugin:
            def get_port(self):
                return 30000
        plugin_manager = PluginManager(Plugin(), lambda: None)
        plugin_manager.start()
        time.sleep(1)
        plugin_manager.stop()
        plugin_manager.join()
        self.assertFalse(plugin_manager.is_alive())

