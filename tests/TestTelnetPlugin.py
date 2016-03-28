from unittest import TestCase
from plugins.telnet_plugin import Plugin
import socket


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
        # test is error is thrown, not sure how
        # test a session, use mock
        plugin = Plugin()
        username = 'some_username'
        passed_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        passed_socket.connect(('localhost', plugin.get_port()))
        # It asks for a username and tests if it's the same.(I hope)
        passed_socket.sendall(username)
        un_returned = passed_socket.recv(64)
        self.assertEquals(username, un_returned, 'Test Passed')
        # passes a password and check if it's returned(i think this is the logic)
        password = 'some_password'
        passed_socket.sendall(password)
        password2 = passed_socket.recv(64)
        self.assertEquals(password, password2, 'Test Passed')
        passed_socket.close()

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
