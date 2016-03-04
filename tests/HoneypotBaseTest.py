import unittest
import HoneypotBase


class MyTestCase(unittest.TestCase):
    # plugins tests

    # make sure threads are being created for each plugin
    def test_plugins_loaded(self):
        HoneypotBase._load_plugins()
        self.assertIsNotNone(HoneypotBase.threads)
        self.assertNotEqual(len(HoneypotBase.threads), 0)

    # make sure all plugin manager threads are running
    def test_num_threads_started(self):
        HoneypotBase._load_plugins()
        count = 0
        for i in HoneypotBase.threads:
            if i.isAlive:
                count += 1
        self.assertNotEqual(len(HoneypotBase.threads), 0)
        self.assertEqual(len(HoneypotBase.threads), count)
        # listen user commands

    # stop program
    def test_num_threads_running(self):
        HoneypotBase._load_plugins()
        HoneypotBase._stop_hp()
        count = 0
        for i in HoneypotBase.threads:
            if i.isAlive:
                count += 1
        self.assertNotEqual(len(HoneypotBase.threads), 0)
        self.assertEqual(0, count)

    def test_system_exit(self):
        self.assertEqual(HoneypotBase._stop_hp, True)

if __name__ == '__main__':
    unittest.main()
