from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from geoip import geolite2

Base = declarative_base()


class Telnet(Base):
    __tablename__ = 'telnet'
    id = Column(Integer, primary_key=True)
    username1 = Column(String)
    username2 = Column(String)
    username3 = Column(String)
    password1 = Column(String)
    password2 = Column(String)
    password3 = Column(String)
    geo_ip = Column(String)


class Plugin:

    ORM = {"table": {"table_name": "telnet",
                     "column": [{"name": "username", "type": "TEXT"},
                                {"name": "password", "type": "TEXT"},
                                {"name": "ip", "type": "TEXT"}]
                     }}

    def __init__(self):
        # print "Module Loaded and waiting on run() command"
        self.geo_ip = None
        self.passwords = []
        self.count = 0
        self.username = []
        self.PORT = 8888

    def display(self):
        return self

    def get_description(self):
        info = ("This plugin uses the telnet port to listen how attackers try to attack the telnet specific port."
                + " It gives three attempts to a username and password and store the information in a sql database.")
        return info

    def run(self, socket, address, session):
        # print("Port Number: " + socket.getsockname()[0])
        socket.settimeout(35)
        if socket:
            # for loop and try catch the timeout exception
            username = []
            password = []
            for i in range(0, 3):
                # look into clearing the buffer to read and write
                socket.sendall("username:")
                try:
                    # this sets the timeout and times out after 35 seconds
                    username = socket.recv(64)
                except socket.timeout:
                    print 'timeout error'
                else:
                    # otherwise it receives the data and shuts the timeout off
                    username[i] = socket.recv(64)
                    socket.settimeout(None)
                    self.username.append(username)
                print 'username' + username
                socket.sendall("Password: ")
                try:
                    password[i] = socket.recv(64)
                except socket.timeout:
                    print 'timeout error'
                else:
                    password = socket.recv(64)
                    # socket.settimeout(None)
                    self.passwords.append(password)
                print 'Password : ' + password
                socket.sendall("---Incorrect--\n")
                # socket.sendall("Password: ")
                self.count += 1

            socket.close()
            # record all the information within columns of the db table
            # commit all the information from the session
            record = Telnet(username1=username[0], username2=username[1],username3=username[2],
                            password1=password[0], password2 = password[1], password3=password[2],
                            geo_ip=self.get_geo_ip(address[0]))
            session.add(record)
            session.commit()
            session.close()
        else:
            print "socket error"

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def get_geo_ip(self, host):
        # should use Josh's code for the json conversion and the ip conversion
        match = geolite2.lookup(host)
        self.geo_ip = match.location  # (latitude, longitude)
        return self.geo_ip

