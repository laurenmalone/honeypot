from sqlalchemy import Column, Integer, String, DateTime
from plugin_template import Template
from base import Base
from select import select
from string import join
import json
import logging
import datetime


class Plugin(Template):
    """ Listens on Telnet Plugin for client-server responses. Adds data to database.

    Inherit Template from plugin_template.py --convert_to_geojson_feature,
    display, description, orm, port
    """

    def __init__(self):
        Template.__init__(self)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.value = "telnet"
        self.display = "Telnet"
        self.PORT = 23
        self.description = ("This plugin uses the telnet port to listen for attackers. "
                            "It allows a user to login and then record upto 5 commands from the user"
                            " and stores the information in a sql database.")
        self.ORM = json.dumps({
            "table": {
                "table_name": "telnet",
                "column": [
                    {"name": "username", "type": "TEXT"},
                    {"name": "password", "type": "TEXT"},
                    {"name": "commands", "type": "TEXT"},
                    {"name": "feature", "type": "TEXT"},
                    {"name": "ip_address", "type": "TEXT"},
                    {"name": "time_stamp", "type": "TEXT"}
                ]
            }
        })

    class Telnet(Base):
        __tablename__ = "telnet"
        id = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        commands = Column(String)
        feature = Column(String)
        ip_address = Column(String)
        time_stamp = Column(DateTime)

    def run(self, client_socket, address, session):
        """ Listens for a username, password, and commands
            from a user for attack. Converts geoIP
            addresses for record. Records and sends to DB.

        :param client_socket: connection to client
        :param address: client address
        :param session: session for DB communication
        :return: record with the geoIP conversions
        Raises exception if timeout occurs.
        """
        logging.info(self.time_stamp)
        timeout = 10
        if client_socket:
            client_socket.setblocking(0)
            while select([client_socket], [], [], 2)[0]:
                client_socket.recv(1024) # discard negotiation sequences
            client_socket.sendall("login as: ")
            if select([client_socket], [], [], timeout)[0]:
                username = client_socket.recv(256).strip()
                logging.info(str(datetime.datetime.now()) + ': Login information obtained')
            else:
                username = 'invalid input'
                logging.error(str(datetime.datetime.now()) + ': timed out on username')
                client_socket.sendall("\n")
            # login string as shell script style
            login_string = username + "@73.78.8.177's " + "password: "
            client_socket.sendall(login_string)
            if select([client_socket], [], [], timeout)[0]:
                password = client_socket.recv(256).strip()
            else:
                password = 'timeout error'
                logging.error(str(datetime.datetime.now()) + ': timeout error')
                client_socket.sendall("\n")

            commands = []
            for _ in range(5):
                command_string = username + "@73.78.8.177's" + ": "  # command prompt -> 'username@host:path $ '
                client_socket.sendall(command_string)
                if select([client_socket], [], [], timeout)[0]:
                    commands.append(client_socket.recv(256).strip())
                else:
                    commands.append(str(datetime.datetime.now()) + ': timeout error')
                    logging.error(str(datetime.datetime.now()) + ': timeout error')
                    client_socket.sendall("\n")

            client_socket.close()
            logging.info('socket closed ')
            geo_ip_record = self.get_record_from_geoip(address[0])
            if geo_ip_record is not None:
                self.geoIp_feature_json_string = self.convert_to_geojson_feature(geo_ip_record)

            record = self.Telnet(username=username, password=password, commands=join(commands, ', '),
                                 feature=self.get_feature(address[0]), ip_address=address[0],
                                 time_stamp=self.time_stamp)
            session.add(record)
            session.commit()
            session.close()
        else:
            logging.error(str(datetime.datetime.now()) + ': socket error occurred')

