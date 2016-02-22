import unittest


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
        else passed_socket.closed:
            print "Throws Error Message"
            print "Test Failed"
            #self.assertEquals(passed_socket.ip, ipresult, 'Test Passed')
            # needs to test sleep time
            # message1 = 'username: '
            # message2 = 'password: '

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM
