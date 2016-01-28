class Plugin:

    import socket
    import sys

    PORT = 8888

    def __init__(self):
        print "Module Loaded and waiting on run() command"

    def run(self, passed_socket):
        print("Port Number: " + passed_socket.getsockname()[0])
        if passed_socket:
            passed_socket.listen(10)
            while 1:
                conn, address = passed_socket.accept()
                print 'Connecting with ' + address[0] + ':' + str(address[1])
                print 'socket family: ' + str(passed_socket.family)
                print 'socket type: ' + str(passed_socket.type)
                print 'socket proto: ' + str(passed_socket.proto)
                conn.sendall("Login: ")
                login = conn.recv(64)
                print 'Login : ' + login
                conn.sendall("Password: ")
                password = conn.recv(64)
                print 'Password : ' + password
            passed_socket.close()
        else:
            print "socket error"

    def get_port(self):
        return self.PORT