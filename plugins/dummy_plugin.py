from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import GeoIP
import geojson
import json
import datetime



class Plugin:

    def __init__(self):
        # print "Module Loaded and waiting on run() command"
        self.display = "Dummy Plugin"
        self.PORT = 9006
        self.description = "This is a dummy plugin used to test connections to ports that are unused by other plugins"
        self.geoIp_feature_json_string = ""
        self.stream_input = ""
        self.geoIpDB = GeoIP.open("./GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
        self.time_stamp = ''
        self.orm = {"table": {"table_name": "Dummy",
                     "column":[{"name": "ip_address", "type": "TEXT"},
                               {"name": "port_number", "type": "TEXT"},
                               {"name": "feature", "type": "TEXT"},
                               {"name": "stream", "type": "TEXT"}]
                     }}

    class Dummy(Base):
        __tablename__ = 'dummy'
        id = Column(Integer, primary_key=True)
        ip_address = Column(String)
        port_number = Column(String)
        feature = Column(String)
        stream = Column(String)
        time_stamp = Column(DateTime)

    def run(self, socket, address, session):
        print "dummy ip", address
        self.stream_input = socket.recv(64)
        socket.close()
        self.time_stamp = datetime.datetime.now()
        geo_ip_record = self.get_record_from_geoip(address[0])
        if geo_ip_record is not None:
            self.geoIp_feature_json_string = self.convert_to_geojson_feature(geo_ip_record)
        try:
            session.add(self.Dummy(ip_address=address[0], port_number=str(self.PORT),
                                   feature=self.geoIp_feature_json_string, stream=self.stream_input,
                                   time_stamp=self.time_stamp))
            session.commit()
        except RuntimeError:
            print "Error Saving Data: "
            pass
        session.close()

    def get_port(self):
        return self.PORT

    def set_port(self, port_number):
        self.PORT = port_number

    def get_description(self):
        return self.description

    def get_display(self):
        return self.display

    def convert_to_geojson_feature(self, ip_record):
        # print ip_record
        self.convert_to_geojson_point(ip_record)
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
            "country_name": ip_record["country_name"],
            "time_stamp": ('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(self.time_stamp))
        }
        #print "feature", feature
        feature_string = json.dumps(feature)
        #print "featureString", feature_string
        #print 'str', str(feature)
        return feature_string

    def convert_to_geojson_point(self, ip_record):
        #print "ip_record", ip_record
        return geojson.Point((ip_record["latitude"], ip_record["longitude"]))

    def get_record_from_geoip(self, ip_address):
        #print "ip_address", ip_address
        #the IP Address is hard coded for testing. Need to add
        #TODO
        record = self.geoIpDB.record_by_name(ip_address)
        #print "record", record
        return record

    def get_orm(self):
        return self.orm