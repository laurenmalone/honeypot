import sys


class Plugin:
    ORM = {"table": {
        'tableName': "test_table2",
        "column": {
            "name": "ip",
            "type": "TEXT",
        }
    }}

    def __init__(self):
        print "Module Loaded and waiting on run() command"
        self.sqliteDbConn = None
        self.geoIp = None
        self.passwords = []
        self.count = 0
        self.login = ""
        self.PORT = 8888

    def run(self, passed_socket):
        # print("Port Number: " + passed_socket.getsockname()[0])
        if passed_socket:
            passed_socket.listen(10)
            while 1:
                conn, address = passed_socket.accept()
                print 'Connecting with ' + address[0] + ':' + str(address[1])
                print 'socket family: ' + str(passed_socket.family)
                print 'socket type: ' + str(passed_socket.type)
                print 'socket proto: ' + str(passed_socket.proto)
                conn.sendall("Login: ")
                self.login = conn.recv(64)
                # need to sleep thread if no answer
                print 'Login : ' + self.login
                while self.count < 3:
                    conn.sendall("Password: ")
                    password = conn.recv(64)
                    self.passwords.append(password)
                    print 'Password : ' + password
                    conn.sendall("---Incorrect--\n")
                    conn.sendall("Password: ")
                    self.count += 1
            passed_socket.close()
            sys.exit(0)
        else:
            print "socket error"

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def set_db_conn(self, conn):
        self.sqliteDbConn = conn

    def set_geoip(self, geoip):
        self.geoIp = geoip
