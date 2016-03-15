from unittest import TestCase
from plugins.telnet_plugin import Plugin


class TestTelnetPlugin(TestCase):
    PORT = 8888
    ORM = {"table": {
        'tableName': "test_table1",
        "column": {
            "name": "ip",
            "type": "TEXT"
        }
    }}

    # def __init__(self):
    # print("plugin Test init")

    def test_plugin_run(self, passed_socket, session):
        # if a closed connection is passed, drop socket.
        result = 8080
        self.assertEquals(passed_socket.port, result, 'Test Passed')
        self.assertRaises(IOError, lambda: Plugin().run('Closed Connection Passed'))

        # test a session, use mock
            # needs to test sleep time

            # message1 = 'username: '
            # message2 = 'password: '

    def test_port(self):
        return self.PORT

    def test_orm(self):
        ip_result = ''
        self.assertEquals(self.ORM, ip_result, True)
        return self.ORM

    def test_geo_ip(self):
        geo_result = ''
        self.assertEquals(self.get_geo_ip(), geo_result, True)
        return self.get_geo_ip()
