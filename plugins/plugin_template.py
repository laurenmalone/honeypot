import GeoIP
import json
import geojson
import datetime


class Template(object):

    def __init__(self):
        self.geo_ip = None
        self.PORT = 0
        self.geoIp_feature_json_string = None
        self.giDB = GeoIP.open("./GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
        self.description = None
        self.ORM = None
        self.value = None
        self.display = None
        self.time_stamp = None
    def get_port(self):
        return self.PORT

    def get_orm(self):
        return self.ORM

    def get_value(self):
        return self.value

    def get_display(self):
        return self.display

    def get_description(self):
        return self.description

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

        feature_string = json.dumps(feature)
        return feature_string

    def get_feature(self, address):
        record = self.get_record_from_geoip(address)
        if record is not None:
            return self.convert_to_geojson_feature(record)
        else:
            return None



