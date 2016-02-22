import unittest
from HoneypotBase import HoneypotBase


class MyTestCase(unittest.TestCase):
    # plugins tests

    # invalid plugin directory
    def test_plugins_found(self):
        self.assertRaises(IOError, lambda: HoneypotBase().load_plugins('path_doesnt_exist'))

    # invalid plugin files
    def test_plugins_valid(self):
        self.assertRaises(IOError, lambda: HoneypotBase().load_plugins('bad_plugins'))

    # make sure threads are being created for each plugin
    def test_plugins_loaded(self):
        HoneypotBase.load_plugins('plugins')
        self.assertIsNotNone(HoneypotBase.threads)
        self.assertNotEqual(len(HoneypotBase.threads), 0)

    # make sure all plugin manager threads are running
    def test_num_threads_started(self):
        HoneypotBase.load_plugins('plugins')
        count = 0
        for i in HoneypotBase.threads:
            if i.isAlive:
                count += 1
        self.assertNotEqual(len(HoneypotBase.threads), 0)
        self.assertEqual(len(HoneypotBase.threads), count)
        # listen user commands

    # stop program
    def test_num_threads_running(self):
        HoneypotBase.load_plugins('plugins')
        HoneypotBase.stop()
        count = 0
        for i in HoneypotBase.threads:
            if i.isAlive:
                count += 1
        self.assertNotEqual(len(HoneypotBase.threads), 0)
        self.assertEqual(0, count)

    def test_system_exit(self):
        self.assertEqual(HoneypotBase.stop(), True)

if __name__ == '__main__':
    unittest.main()
