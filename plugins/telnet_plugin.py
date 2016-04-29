from sqlalchemy import Column, Integer, String, DateTime
from plugin_template import Template
from base import Base
from string import join
import socket
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

    def run(self, passed_socket, address, session):
        """ Sets a 35 sec. timeout. Listens for a username, password,
            and commands from a user for attack. Converts geoIP addresses for record.
            Records and sends to DB.

        :param passed_socket: connection to client
        :param address: client address
        :param session: session for DB communication
        :return: record with the geoIP conversions
        Raises exception if timeout occurs.
        """
        logging.info(self.time_stamp)
        if passed_socket:
            passed_socket.settimeout(35)
            passed_socket.sendall("login as: ")
            try:
                username = passed_socket.recv(4096)
                username.strip()
                logging.info(str(datetime.datetime.now()) + ': Login information obtained')
            except socket.timeout:
                passed_socket.sendall('timeout error')
                username = 'invalid input'
                logging.error(str(datetime.datetime.now()) + ': invalid input error')
                passed_socket.sendall("\n")
                # login string as shell script style
            login_string = username + "@73.78.8.177's " + "password: "
            passed_socket.sendall(login_string)
            try:
                password = passed_socket.recv(64)
                password.strip()
            except socket.timeout:
                password = 'timeout error'
                passed_socket.sendall("\n")
                logging.error(str(datetime.datetime.now()) + ': timeout error')

            commands = []
            for _ in range(5):
                command_string = username + "@73.78.8.177's" + ": "  # command prompt -> 'username@host:path $ '
                passed_socket.sendall(command_string)
                try:
                    command = passed_socket.recv(64)
                    command.strip()
                    commands.append(command)
                except socket.timeout:
                    commands.append(str(datetime.datetime.now()) + ': timeout error')
                    passed_socket.sendall("\n")
                    logging.error(str(datetime.datetime.now()) + ': timeout error')

            passed_socket.close()
            logging.info('socket closed ')
            geo_ip_record = self.get_record_from_geoip(address[0])
            if geo_ip_record is not None:
                self.geoIp_feature_json_string = self.convert_to_geojson_feature(geo_ip_record)

            record = self.Telnet(username=username, password=password, commands=join(commands, ', '),
                                 feature=self.geoIp_feature_json_string, ip_address=address[0],
                                 time_stamp=self.time_stamp)
            session.add(record)
            session.commit()
            session.close()
        else:
            logging.error(str(datetime.datetime.now()) + ': socket error occurred')
