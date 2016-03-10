from unittest import TestCase
import HoneypotBase
import time

class TestHoneypotBase(TestCase):



    def test_num_threads_stopped_using_kill(self):
        print "test kill"
        self.assertTrue(HoneypotBase._load_plugins())
        #self.assertTrue(HoneypotBase._add_plugin_table())
        self.assertTrue(HoneypotBase._create_plugin_tables())
        HoneypotBase._start_manager_threads()
        time.sleep(0.01)
        HoneypotBase._signal_handler('15', None)
        for i in HoneypotBase.threads:
            self.assertFalse(i.is_alive())


    """def test_num_threads_started(self):
        print"test num threads started"
        self.assertTrue(HoneypotBase._load_plugins())
        #self.assertTrue(HoneypotBase._add_plugin_table())
        self.assertTrue(HoneypotBase._create_plugin_tables())
        HoneypotBase._start_manager_threads()
        self.assertEqual(len(HoneypotBase.threads), len(HoneypotBase.plugin_list))

        for i in HoneypotBase.threads:
            self.assertTrue(i.is_alive())
        HoneypotBase._signal_handler('15', None)
        time.sleep(1)

    def test_load_plugins(self):
        print "test load plugins"
        self.assertTrue(HoneypotBase._load_plugins())
        HoneypotBase._signal_handler('15', None)

    def test_already_used(self):
        print "test already used"

        class Plugin():
            def __init__(self, port):
                self._port = port

            def get_port(self):
                return self._port

        HoneypotBase.plugin_list = [Plugin(80), Plugin(23), Plugin(25)]
        self.assertTrue(HoneypotBase._port_already_used(80))
        self.assertTrue(HoneypotBase._port_already_used(23))
        self.assertTrue(HoneypotBase._port_already_used(25))
        self.assertFalse(HoneypotBase._port_already_used(90))
        self.assertFalse(HoneypotBase._port_already_used(10))
        HoneypotBase._signal_handler('15', None)

    def test_invalid_ports(self):
        # 0, 65535
        pass



    def test_num_threads_stopped_using_ctrlc(self):
        print "test ctrlc"
        self.assertTrue(HoneypotBase._load_plugins())
        #self.assertTrue(HoneypotBase._add_plugin_table())
        self.assertTrue(HoneypotBase._create_plugin_tables())
        HoneypotBase._start_manager_threads()
        time.sleep(0.01)
        HoneypotBase._signal_handler('^C2', None)
        for i in HoneypotBase.threads:
            self.assertFalse(i.is_alive())


    #def test_bad_plugins_directory(self):
        #HoneypotBase.plugin_directory = '/test_plugins'
        #self.assertFalse(HoneypotBase._load_plugins())
        #HoneypotBase._signal_handler('15', None)

    # def test_bad_plugin(self):
        pass
     """