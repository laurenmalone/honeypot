from unittest import TestCase
import HoneypotBase
import time


class TestHoneypotBase(TestCase):

    def setUp(self):

        HoneypotBase.plugin_directory = 'plugins/'
        HoneypotBase.threads = []
        HoneypotBase.plugin_list = []

    def test_num_threads_stopped_using_kill(self):

        self.assertTrue(HoneypotBase._load_plugins())
        HoneypotBase._start_manager_threads()
        time.sleep(0.01)
        HoneypotBase._signal_handler('15', None)
        for i in HoneypotBase.threads:
            self.assertFalse(i.is_alive())

    def test_num_threads_stopped_using_ctrlc(self):

        self.assertTrue(HoneypotBase._load_plugins())
        del(HoneypotBase.threads[:])
        HoneypotBase._start_manager_threads()
        time.sleep(0.01)
        HoneypotBase._signal_handler('^C2', None)
        for i in HoneypotBase.threads:
            self.assertFalse(i.is_alive())

    def test_port_valid(self):

        class Plugin():
            def __init__(self, port):
                self._port = port

            def get_port(self):
                return self._port

        HoneypotBase.plugin_list = [Plugin(80), Plugin(23), Plugin(25)]
        self.assertFalse(HoneypotBase._port_valid(80))
        self.assertFalse(HoneypotBase._port_valid(23))
        self.assertFalse(HoneypotBase._port_valid(25))
        self.assertTrue(HoneypotBase._port_valid(90))
        self.assertTrue(HoneypotBase._port_valid(0))
        self.assertTrue(HoneypotBase._port_valid(10))
        self.assertTrue(HoneypotBase._port_valid(0))
        HoneypotBase._signal_handler('15', None)

    def test_load_plugins(self):

        self.assertTrue(HoneypotBase._load_plugins())
        HoneypotBase._signal_handler('15', None)

    def test_bad_plugins_directory(self):
        HoneypotBase.plugin_directory = '/test_plugins'
        self.assertFalse(HoneypotBase._load_plugins())
        HoneypotBase._signal_handler('15', None)

    def test_add_table(self):
        self.assertTrue(HoneypotBase._add_plugin_table())


    def test_create_table(self):
        self.assertTrue(HoneypotBase._create_plugin_tables())








    """# def test_bad_plugin(self):
        pass
     """