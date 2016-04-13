from sqlalchemy import Column, Integer, String, DateTime
from base import Base
from string import join
import GeoIP
import geojson
import socket
import json
import datetime
import logging


class Plugin:
    
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        # print "Module Loaded and waiting on run() command"
        self.geo_ip = None
        self.PORT = 23
        self.geoIp_feature_json_string = None
        self.giDB = GeoIP.open("./GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
        self.info = ("This plugin uses the telnet port to listen for attackers. "
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

        self.time_stamp = ''
        self.value = "telnet"
        self.display = "Telnet"

    class Telnet(Base):
        __tablename__ = "telnet"
        id = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        commands = Column(String)
        feature = Column(String)
        ip_address = Column(String)
        time_stamp = Column(DateTime)

    def get_display(self):
        return self.display

    def run(self, passed_socket, address, session):
        
        self.time_stamp = datetime.datetime.now()
        logging.info(self.time_stamp)
        # passed_socket.recv(2048, flags=socket.MSG_TRUNC)
        passed_socket.settimeout(35)
        if socket:
            # check Stephen's about how he stops negotiating inputs
            passed_socket.sendall("login as: ")
            try:
                # data = passed_socket.recv(4096)
                # if(data in '\\xff' || '\\xfb' || '\\x1f' || '\\x18' || '\\x01' || '\\x03' || '\\xfd' || '\\xfe' || '\\xfc')
                 username = passed_socket.recv(4096)
                username.strip()
                logging.info('Login information obtained')
            except socket.timeout:
                print 'timeout error'
                passed_socket.sendall('timeout error')
                username = 'invalid input'
                logging.error('invalid input error')
                passed_socket.sendall("\n")
                # login string as shell script style
            login_string = username + "@73.78.8.177's " + "password: "
            passed_socket.sendall(login_string)
            try:
                password = passed_socket.recv(64)
                password.strip()
            except socket.timeout:
                print 'timeout error'
                password = 'timeout error'
                passed_socket.sendall("\n")

            commands = []
            for _ in range(5):
                command_string = username + "@73.78.8.177's" + ": "  # command prompt -> 'username@host:path $ '
                passed_socket.sendall(command_string)
                try:
                    command = passed_socket.recv(64)
                    command.strip()
                    commands.append(command)
                except socket.timeout:
                    print 'timeout error'
                    commands.append('timeout error')
                    passed_socket.sendall("\n")

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
            print "socket error"
            logging.error('socket error occurred')

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def get_record_from_geoip(self, ip_address):
        # print "ip_address", ip_address
        # the IP Address is hard coded for testing. Need to add
        # TODO
        record = self.giDB.record_by_name(ip_address)
        # print "record", record
        return record

    def convert_to_geojson_point(self, ip_record):
        return geojson.Point((ip_record["latitude"], ip_record["longitude"]))

    def convert_to_geojson_feature(self, ip_record):
        feature = geojson.Feature(geometry=self.convert_to_geojson_point(ip_record))
        feature["properties"] = {
            "city": ip_record["city"],
            "region_name": ip_record["region_name"],
            "reg@on": ip_record["region"],
            "area_code": ip_record["area_code"],
            "time_zone": ip_record["time_zone"],
            "metro_code": ip_record["metro_code"],
            "country_code3": ip_record["country_code3"],
            "postal_code": ip_record["postal_code"],
            "dma_code": ip_record["dma_code"],
            "country_code": ip_record["country_code"],
            "country_name": ip_record["country_name"],
            "time_stamp": ('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(self.time_stamp))
        }
        logging.info('sent information')

        feature_string = json.dumps(feature)
        return feature_string

    def get_description(self):
        return self.info

    def get_value(self):
        return self.value
