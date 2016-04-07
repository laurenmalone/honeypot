from unittest import TestCase
from plugins.http_plugin import Plugin
import HoneypotBase
from httplib import HTTPConnection
from PluginManager import PluginManager
import time


class TestHttpPlugin(TestCase):
    def setUp(self):
        HoneypotBase.read_config()
        self.thread = PluginManager(Plugin(), HoneypotBase.Session)
        self.thread.start()
        time.sleep(.1)

    def tearDown(self):
        self.thread.stop()

    def test_insert_valid_record_1(self):
        record = Plugin.Http(ip_address='41.161.65.153', command='GET', path='/', version=1.0, headers=None, time=None,
                             feature= Plugin().get_feature('41.161.65.153'))
        self.assertTrue(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_insert_record_where_address_is_null(self):
        record = Plugin.Http(ip_address=None, command='GET', path='/index.htm', version=1.1,
                             headers=None, time=None, feature=None)
        self.assertFalse(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_insert_record_where_feature_is_unknown(self):
        record = Plugin.Http(ip_address='localhost', command='POST', path='/index.htm', version=6,
                             headers=None, time=None, feature=Plugin().get_feature('localhost'))
        self.assertTrue(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_insert_valid_record_3(self):
        record = Plugin.Http(ip_address='181.161.28.209', command='POST', path='/', version=6,
                             headers=None, time=None, feature='181.161.28.209')
        self.assertTrue(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_insert_record_where_path_is_none(self):
        record = Plugin.Http(ip_address='177.82.42.192', command='POST', path=None, version=6,
                             headers=None, time=None, feature=Plugin().get_feature('177.82.42.192'))
        self.assertTrue(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_insert_record_where_command_is_none(self):
        record = Plugin.Http(ip_address='177.82.42.192', command=None, path=None, version=6,
                             headers=None, time=None, feature=Plugin().get_feature('177.82.42.192'))
        self.assertTrue(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_insert_record_where_command_isnt_supported(self):
        record = Plugin.Http(ip_address='177.82.42.192', command='get', path=None, version=6,
                             headers=None, time=None, feature=Plugin().get_feature('177.82.42.192'))
        self.assertTrue(Plugin.insert_record(Plugin(), record, HoneypotBase.Session()))

    def test_response_unsupported_method(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request(None, "/")
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 501)

    def test_response(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request("GET", None)
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 400)

    def test_response1(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request("GET", "")
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 400)
        
    def test_response_1(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request("DELETE", None)
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 400)

    def test_response_2(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request("POST", None)
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 400)

    def test_response_valid_request(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request("GET", "/")
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 400)

    def test_response_bad_status_line(self):
        conn = HTTPConnection('localhost', 9999, True)
        conn.request("get", "/")
        res = conn.getresponse()
        res.read()
        conn.close()
        self.assertEqual(res.status, 501)



