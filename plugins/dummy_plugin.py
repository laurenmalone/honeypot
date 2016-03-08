from sqlalchemy import Column, Integer, String
#from HoneypotBase import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Plugin:

    def __init__(self):
        # print "Module Loaded and waiting on run() command"
        self.geo_ip = None
        self.passwords = []
        self.count = 0
        self.username = []
        self.PORT = 33333

    class Dummy(Base):
        __tablename__ = 'dummy'
        id = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)

    def run(self, socket, address, session):
        socket.close()
        session.add(self.Dummy(username = 'gdejohn4', password='qwerty'))
        session.commit()
        session.close()

    def get_port(self):
        return self.PORT

