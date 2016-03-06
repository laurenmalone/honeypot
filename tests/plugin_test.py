import unittest
import geoIp

class PluginTest(unittest.TestCase):
    PORT = 8080
    ORM = {"table": {
        'tableName': "test_table1",
        "column": {
            "name": "ip",
            "type": "TEXT"
        }
    }}

    # def __init__(self):
        #print("plugin Test init")

    def PluginTestrun(self, passed_socket):
        # if a closed connection is passed, drop socket.
        result = 8080
        if self.assertEquals(passed_socket.port, result, 'Test Passed'):
        else:
            self.assertRaises(IOError, lambda: Plugin().run('Closed Connection Passed'):
            print 'failed'
            # needs to test sleep time
            # message1 = 'username: '
            # message2 = 'password: '

    def get_port(self):
        return self.PORT

    def get_orm(self):
        ip_result = ''
        self.assertEquals(self.ORM , ip_result, True)
        return self.ORM
