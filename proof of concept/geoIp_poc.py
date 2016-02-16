# You will need to install python packages python-geoip, python-pip, and python-wheel
# Debian "jessie" commands:
# apt-get install python-geoip
# apt-get install python-pip python-wheel
# pip install geojson

import GeoIP
import geojson

giDB = GeoIP.open("geoIP/GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)


def convert_to_geojson_point(ip_record):
    return geojson.Point((ip_record["latitude"], ip_record["longitude"]))


def convert_to_geojson_feature(ip_record):
    # print ip_record
    convert_to_geojson_point(ip_record)
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


def get_record_from_geoip(ip_address):
    return giDB.record_by_name(ip_address)

record = get_record_from_geoip("71.205.10.208")

print record
print convert_to_geojson_point(record)
print convert_to_geojson_feature(record)