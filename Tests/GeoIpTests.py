import unittest
from geoIp import get_record_from_geoip, convert_to_geojson_point, convert_to_geojson_feature



class TestGeoIpMethods(unittest.TestCase):

    def test_geoip_decoder(self):
        self.assertEquals(get_record_from_geoip(
                "71.205.10.208"),
                {'city': 'Arvada',
                    'region_name': 'Colorado', 'region': 'CO',
                    'area_code': 303,
                    'time_zone': 'America/Denver',
                    'longitude': -105.06069946289062,
                    'metro_code': 751,
                    'country_code3': 'USA',
                    'latitude': 39.828800201416016,
                    'postal_code': '80003',
                    'dma_code': 751,
                    'country_code': 'US',
                    'country_name': 'United States'
                 }
        )

    def test_geoip_result_point(self):
        result = get_record_from_geoip("71.205.10.208")
        self.assertEquals(convert_to_geojson_point(result),
                          {"coordinates": [39.828800201416016, -105.06069946289062], "type": "Point"})


    def test_geoip_result_feature(self):
        result = get_record_from_geoip("71.205.10.208")
        self.assertEquals(convert_to_geojson_feature(result),
                          {"geometry": {"coordinates": [39.828800201416016, -105.06069946289062], "type": "Point"},
                           "properties": {"area_code": 303, "city": "Arvada", "country_code": "US",
                                          "country_code3": "USA", "country_name": "United States",
                                          "dma_code": 751, "metro_code": 751, "postal_code": "80003", "region": "CO",
                                          "region_name": "Colorado", "time_zone": "America/Denver"}, "type": "Feature"})


    def test_geoip_decoder2(self):
        self.assertNotEqual(get_record_from_geoip(
                "71.205.10.208"),
                {'city': 'Arvada',
                    'region_name': 'Colorado', 'region': 'CO',
                    'area_code': 304,
                    'time_zone': 'America/Denver',
                    'longitude': -105.06069946289062,
                    'metro_code': 751,
                    'country_code3': 'USA',
                    'latitude': 39.828800201416016,
                    'postal_code': '80003',
                    'dma_code': 751,
                    'country_code': 'US',
                    'country_name': 'United States'
                 }
        )

    def test_geoip_result_point2(self):
        result = get_record_from_geoip("71.205.10.208")
        self.assertNotEquals(convert_to_geojson_point(result),
                          {"coordinates": [38.828800201416016, -105.06069946289062], "type": "Point"})

    def test_geoip_result_feature2(self):
        result = get_record_from_geoip("71.205.10.208")
        self.assertNotEquals(convert_to_geojson_feature(result),
                          {"geometry": {"coordinates": [39.828800201416017, -105.06069946289062], "type": "Point"},
                           "properties": {"area_code": 303, "city": "Arvada", "country_code": "US",
                                          "country_code3": "USA", "country_name": "United States",
                                          "dma_code": 751, "metro_code": 751, "postal_code": "80003", "region": "CO",
                                          "region_name": "Colorado", "time_zone": "America/Denver"}, "type": "Feature"}
                             )