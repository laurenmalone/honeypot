from sqlalchemy import Column, Integer, String
from base import Base
import GeoIP
import geojson
import socket
import json


class Plugin:

    class Telnet(Base):
        __tablename__ = 'telnet'
        id = Column(Integer, primary_key=True)
        username1 = Column(String)
        username2 = Column(String)
        username3 = Column(String)
        password1 = Column(String)
        password2 = Column(String)
        password3 = Column(String)
        feature = Column(String)
        ip_address = Column(String)


    def __init__(self):
        # print "Module Loaded and waiting on run() command"
        self.geo_ip = None
        self.PORT = 8888
        self.giDB = GeoIP.open("./GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
        self.info = ("This plugin uses the telnet port to listen how attackers try to attack the telnet specific port. "
                     "It gives three attempts to a username and password and store the information in a sql database.")
        self.ORM = {"table": {"table_name": "telnet",
                     "column": [{"name": "username", "type": "TEXT"},
                                {"name": "password", "type": "TEXT"},
                                {"name": "ip", "type": "TEXT"}]
                    }}

    def get_display(self):
        return "telnet"

    def run(self, passed_socket, address, session):
        passed_socket.settimeout(35)
        if socket:
            # for loop and try catch the timeout exception
            usernames = []
            passwords = []
            for _ in range(3):
                # look into clearing the buffer to read and write
                passed_socket.sendall("Username: ")
                try:
                    usernames.append(passed_socket.recv(64))
                except socket.timeout:
                    print 'timeout error'
                    usernames.append('timeout error')
                    passwords.append('timeout error')
                    continue
                passed_socket.sendall("Password: ")
                try:
                    passwords.append(passed_socket.recv(64))
                except socket.timeout:
                    print 'timeout error'
                    passwords.append('timeout error')
                passed_socket.sendall("---Incorrect--\n")

            passed_socket.close()
            # record all the information within columns of the db table
            # commit all the information from the session
            record = self.Telnet(username1=usernames[0], username2=usernames[1], username3=usernames[2],
                                 password1=passwords[0], password2=passwords[1], password3=passwords[2],
                                 feature=self.get_geo_ip(address[0], ip_address=address[0]))
            session.add(record)
            session.commit()
            session.close()
        else:
            print "socket error"

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def get_geo_ip(self, ip_address):
        return self.giDB.record_by_name(ip_address)

    def convert_to_geojson_point(self, ip_record):
        return geojson.Point((ip_record["latitude"], ip_record["longitude"]))

    def convert_to_geojson_feature(self, ip_record):
        feature = geojson.Feature(geometry=self.convert_to_geojson_point(ip_record))
        feature["properties"] = {
            "city": ip_record["city"],
            "region_name": ip_record["region_name"],
            "region": ip_record["region"],
            "area_code": ip_record["area_code"],
            "time_zone": ip_record["time_zone"],
            "metro_code": ip_record["metro_code"],
            "country_code3": ip_record["country_code3"],
            "postal_code": ip_record["postal_code"],
            "dma_code": ip_record["dma_code"],
            "country_code": ip_record["country_code"],
            "country_name": ip_record["country_name"]
        }

        feature_string = json.dumps(feature)
        return feature_string

    def get_description(self):
        return self.info
