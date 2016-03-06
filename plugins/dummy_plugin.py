from sqlalchemy import Column, Integer, String
from HoneypotBase import Base

class Dummy(Base):
    __tablename__ = 'dummy'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password =  Column(String)

class Plugin:
    def run(self, socket, address, session):
        socket.close()
        session.add(Dummy(username = 'gdejohn', password='qwerty'))
        session.commit()
        session.close()

    def get_port(self):
        return 38746

