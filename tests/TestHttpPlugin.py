from unittest import TestCase
from plugins.http_plugin import Plugin
import HoneypotBase
from httplib import HTTPConnection
from PluginManager import PluginManager


class TestHttpPlugin(TestCase):

    def SetUp(self):

        pass

    def TearDown(self):
        pass

    """ def test_get_record(self):

        handler = Plugin().Handler(None, 'localhost',  None)
        address = handler.client_address[0]
        command = handler.command
        path = handler.path
        version = handler.request_version
        headers = str(handler.headers)
        time = Plugin().time_stamp
        feature = Plugin.get_feature(Plugin(), address)"""

    def test_insert_record_1(self):
        record = Plugin.Http(address='localhost', command='GET', path=None, version=1.0,
                             headers=None, time=None, feature=None)
        HoneypotBase._read_config()
        session = HoneypotBase._Session()
        self.assertTrue(Plugin.insert_record(Plugin(), record, session))

    def test_insert_record_2(self):
        record = Plugin.Http(address=None, command='GET', path=None, version=1.1,
                             headers=None, time=None, feature=None)
        HoneypotBase._read_config()
        session = HoneypotBase._Session()
        self.assertFalse(Plugin.insert_record(Plugin(), record, session))

    def test_insert_record_3(self):
        record = Plugin.Http(address='localhost', command='POST', path=None, version=6,
                             headers=None, time=None, feature=None)
        HoneypotBase._read_config()
        session = HoneypotBase._Session()
        self.assertTrue(Plugin.insert_record(Plugin(), record, session))

    def test_response_1(self):
        thread = PluginManager(Plugin(), None)
        thread.start()
        conn = HTTPConnection('localhost', 9999)
        conn.request("GET","/")
        res = conn.getresponse()
        self.assertEqual(res.status, '404')
        self.assertEqual(res.reason, 'Not found')
