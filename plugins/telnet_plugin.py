from sqlalchemy import Column, Integer, String
from base import Base
import GeoIP
import geojson

giDB = GeoIP.open("geoIP/GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)

def convert_to_geojson_point(ip_record):
    return geojson.Point((ip_record["latitude"], ip_record["longitude"]))

def convert_to_geojson_feature(ip_record):
    feature = geojson.Feature(geometry=convert_to_geojson_point(ip_record))
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
    return feature

def get_geo_ip(ip_address):
    return giDB.record_by_name(ip_address)

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
        self.PORT = 8888

    def display(self):
        return "telnet"

    def get_description(self):
        info = ("This plugin uses the telnet port to listen how attackers try to attack the telnet specific port."
                + " It gives three attempts to a username and password and store the information in a sql database.")
        return info

    def run(self, socket, address, session):
        socket.settimeout(35)
        if socket:
            # for loop and try catch the timeout exception
            usernames = []
            passwords = []
            for _ in range(3):
                # look into clearing the buffer to read and write
                socket.sendall("Username: ")
                try:
                    usernames.append(socket.recv(64))
                except socket.timeout:
                    print 'timeout error'
                    usernames.append(None)
                socket.sendall("Password: ")
                try:
                    passwords.append(socket.recv(64))
                except socket.timeout:
                    print 'timeout error'
                    passwords.append(None)
                socket.sendall("---Incorrect--\n")

            socket.close()
            # record all the information within columns of the db table
            # commit all the information from the session
            record = Telnet(username1=usernames[0], username2=usernames[1], username3=usernames[2],
                            password1=passwords[0], password2=passwords[1], password3=passwords[2],
                            geo_ip=get_geo_ip(address[0]))
            session.add(record)
            session.commit()
            session.close()
        else:
            print "socket error"

    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM
