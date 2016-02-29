import unittest
from production.HoneypotBase import HoneypotBase


class MyTestCase(unittest.TestCase):
    # plugins tests

    # make sure threads are being created for each plugin
    def test_plugins_loaded(self):
        hp = HoneypotBase()
        hp._load_plugins()
        self.assertIsNotNone(hp._threads)
        self.assertNotEqual(len(hp._threads), 0)

    # make sure all plugin manager threads are running
    def test_num_threads_started(self):
        hp = HoneypotBase()
        hp._load_plugins()
        count = 0
        for i in HoneypotBase()._threads:
            if i.isAlive:
                count += 1
        self.assertNotEqual(len(hp._threads), 0)
        self.assertEqual(len(hp._threads), count)
        # listen user commands

    # stop program
    def test_num_threads_running(self):
        hp = HoneypotBase()
        hp._load_plugins()
        hp._stop_hp()
        count = 0
        for i in hp._threads:
            if i.isAlive:
                count += 1
        self.assertNotEqual(len(hp._threads), 0)
        self.assertEqual(0, count)

    def test_system_exit(self):
        hp = HoneypotBase()
        self.assertEqual(hp._stop_hp, True)

if __name__ == '__main__':
    unittest.main()
