from sqlalchemy import Column, Integer, String, DateTime
from plugin_template import Template
from base import Base
import GeoIP
import json
import datetime


class Plugin(Template):
    """Listens for connections and records data stream. Closes stream and records data.

    Inherit Template from plugin_template.py
    run(socket, address, session) called by PluginManager
    """
    def __init__(self):
        self.display = "Catch All"
        self.value = "catch_all"
        self.PORT = 81
        self.description = "This is a catch all plugin used to listen on ports that are unused by other plugins"
        self.geoIp_feature_json_string = ""
        self.stream_input = ""
        self.geoIpDB = GeoIP.open("./GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
        self.time_stamp = ''
        self.orm = json.dumps({"table": {"table_name": "catch_all",
                     "column":[{"name": "ip_address", "type": "TEXT"},
                               {"name": "port_number", "type": "TEXT"},
                               {"name": "feature", "type": "TEXT"},
                               {"name": "stream", "type": "TEXT"}]
                     }})

    class CatchAll(Base):
        __tablename__ = "catch_all"
        id = Column(Integer, primary_key=True)
        ip_address = Column(String)
        port_number = Column(String)
        feature = Column(String)
        stream = Column(String)
        time_stamp = Column(DateTime)

    def run(self, socket, address, session):
        """Receives input on stream, closes socket and saves data.

        param: socket -- connection to client
        param: address -- client address
        param: session -- session to communicate with db
        """
        self.stream_input = socket.recv(1024)
        socket.close()
        self.time_stamp = datetime.datetime.now()
        geo_ip_record = self.get_record_from_geoip(address[0])
        if geo_ip_record is not None:
            self.geoIp_feature_json_string = self.convert_to_geojson_feature(geo_ip_record)
        try:
            session.add(self.CatchAll(ip_address=address[0], port_number=str(self.PORT),
                                   feature=self.geoIp_feature_json_string, stream=self.stream_input,
                                   time_stamp=self.time_stamp))
            session.commit()
        except RuntimeError:
            print "Error Saving Data: "
            pass
        session.close()

    def set_port(self, port_number):
        """Sets the port for this catch_all instance.

        param: port_number -- The number of the port to use
        """
        self.PORT = port_number

