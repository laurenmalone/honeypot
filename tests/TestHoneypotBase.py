from unittest import TestCase
import HoneypotBase
import time

class TestHoneypotBase(TestCase):

    def test_1(self):
        HoneypotBase._load_plugins()
        time.sleep(0.01)
        HoneypotBase._signal_handler('15', None)
        #HoneypotBase._signal_handler('^C2', None)
        #'15' - kill, '^C2' - ctrl c

