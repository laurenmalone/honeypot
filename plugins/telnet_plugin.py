import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plugin:

    ORM = {"table": {"table_name": "telnet",
                     "column":[{"name": "username", "type": "TEXT"},
                               {"name": "password", "type": "TEXT"},
                               {"name": "ip", "type": "TEXT"}]
                     }}


    class Telnet(Base):
        __tablename__ = 'telnet'

        id = Column(Integer, primary_key=True)
        username = Column(String)
        password =  Column(String)
        geo_ip =  Column(String)

    def __init__(self):
        # print "Module Loaded and waiting on run() command"
        self.geo_ip = None
        self.passwords = []
        self.count = 0
        self.username = ""
        self.PORT = 8888

    def run(self,passed_socket, address, session):
         # print("Port Number: " + passed_socket.getsockname()[0])
        if passed_socket:
            # need to sleep thread if no answer
            # for loop and try catch the timeout exception
            # while self.count < 3:
            # may have to save the timeout for the next iteration
            for i in range(0,3):
                # try catch
                passed_socket.settimeout(35)
                passed_socket.sendall("username:")
                self.username = passed_socket.recv(64)
                passed_socket.sendall("Password: ")
                password = passed_socket.recv(64)
                self.passwords.append(password)

                # if they take too long to enter password
                # session.add_all([User(username='', password=''),
                #                   User(username='', password='')])
                # session.commit()
                print 'Password : ' + password
                passed_socket.sendall("---Incorrect--\n")
                passed_socket.sendall("Password: ")
                self.count += 1
                record = Telnet(username= '<name>', password = '<password>')
                session.add(record)
                session.commit()
                session.close()
            passed_socket.close()
            sys.exit(0)
        else:
            print "socket error"

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def get_geo_ip(self, passed_socket):
        return self.geo_ip
