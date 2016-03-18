from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import GeoIP
import geojson
import socket
import json
import datetime


class Plugin:
    
    def __init__(self):
        # print "Module Loaded and waiting on run() command"
        self.geo_ip = None
        self.PORT = 8888
        self.geoIp_feature_json_string = ""
        self.giDB = GeoIP.open("./GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
        self.info = ("This plugin uses the telnet port to listen how attackers try to attack the telnet specific port. "
                     "It gives three attempts to a username and password and store the information in a sql database.")
        self.ORM = {"table": {"table_name": "telnet",
                     "column": [{"name": "username", "type": "TEXT"},
                                {"name": "password", "type": "TEXT"},
                                {"name": "ip", "type": "TEXT"}]
                    }}
        self.time_stamp = ''
        self.value = "telnet"
        self.display = "Telnet"
    
    
    class Telnet(Base):
        __tablename__ = "telnet"
        id = Column(Integer, primary_key=True)
        username1 = Column(String)cd
        username2 = Column(String)
        username3 = Column(String)
        password1 = Column(String)
        password2 = Column(String)
        password3 = Column(String)
        feature = Column(String)
        ip_address = Column(String)
        time_stamp = Column(DateTime)

    def get_display(self):
        return self.display

    def run(self, passed_socket, address, session):
        self.time_stamp = datetime.datetime.now()
       #passed_socket.recv(2048, flags=socket.MSG_TRUNC)
        passed_socket.settimeout(35)
        if socket:
            # for loop and try catch the timeout exception
            usernames = []
            passwords = []
            for _ in range(3):
                # look into clearing the buffer to read and write
                login = ''
                password = ''

                passed_socket.sendall("login as: ")
                try:
                    login = passed_socket.recv(64)
                    login.strip()
                    usernames.append(login)
                except socket.timeout:
                    print 'timeout error'
                    usernames.append('timeout error')
                    passwords.append('timeout error')
                    passed_socket.sendall("\n")
                    continue
                login_string = login + "@73.78.8.177's " + "password: "
                passed_socket.sendall(login_string)
                try:
                    passwords.append(passed_socket.recv(64))
                except socket.timeout:
                    print 'timeout error'
                    passwords.append('timeout error')
                    passed_socket.sendall("\n")
                passed_socket.sendall("Access denied\n")

            passed_socket.close()
            geo_ip_record = self.get_record_from_geoip(address[0])
            if geo_ip_record is not None:
                self.geoIp_feature_json_string = self.convert_to_geojson_feature(geo_ip_record)
            # record all the information within columns of the db table
            # commit all the information from the session

            record = self.Telnet(username1=usernames[0], username2=usernames[1], username3=usernames[2],
                                 password1=passwords[0], password2=passwords[1], password3=passwords[2],
                                 feature=self.geoIp_feature_json_string, ip_address=address[0],
                                 time_stamp=self.time_stamp)
            session.add(record)
            session.commit()
            session.close()
        else:
            print "socket error"

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def get_record_from_geoip(self, ip_address):
        #print "ip_address", ip_address
        #the IP Address is hard coded for testing. Need to add
        #TODO
        record = self.giDB.record_by_name(ip_address)
        #print "record", record
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

        feature_string = json.dumps(feature)
        return feature_string

    def get_description(self):
        return self.info

    def get_value(self):
        return self.value
