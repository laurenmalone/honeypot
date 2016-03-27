from plugin_template import Template
from BaseHTTPServer import BaseHTTPRequestHandler
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import json


class Plugin(Template):

    class Http(Base):
        __tablename__ = "http"
        id = Column(Integer, primary_key=True)
        address= Column(String)
        command = Column(String)
        path = Column(String)
        version = Column(String)
        headers = Column(String)
        time = Column(DateTime)
        feature = Column(String)

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):
            pass

        def do_POST(self):
            pass

        def do_OPTIONS(self):
            pass

        def do_HEAD(self):
            pass

        def do_PUT(self):
             pass

        def do_DELETE(self):
            pass

        def do_TRACE(self):
            pass

        def do_CONNECT(self):
            pass

    def __init__(self):
        Template.__init__(self)
        self.value = "http"
        self.display = "Http"
        self.PORT = 9999
        self.description = ("This plugin uses the http port to listen for attackers. "
                            "It returns a 404 not found error to the client "
                            "and stores the information in a sql database.")

        self.ORM = json.dumps({
            "table": {
                "table_name": "http",
                "column": [
                    {"name": "address", "type": "TEXT"},
                    {"name": "command", "type": "TEXT"},
                    {"name": "path", "type": "TEXT"},
                    {"name": "version", "type": "TEXT"},
                    {"name": "headers", "type": "TEXT"},
                    {"name": "time", "type": "TEXT"},
                    {"name": "feature", "type": "TEXT"}

                ]
            }
        })

    def run(self, socket, address, session):

        request_handler = self.Handler(socket, address,  None)

        address = request_handler.client_address[0]
        command = request_handler.command
        path = request_handler.path
        version = request_handler.request_version
        headers = str(request_handler.headers)
        time = self.time_stamp
        feature = self.get_feature(address)

        record = self.Http(address=address, command=command, path=path, version=version,
                           headers=headers, time=time, feature=feature )
        try:
            session.add(record)
            session.commit()
            session.close()
        except Exception:
            print 'error'
