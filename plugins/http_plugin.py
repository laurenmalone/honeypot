from plugin_template import Template
from BaseHTTPServer import BaseHTTPRequestHandler
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import json
import datetime
import logging


class Plugin(Template):
    """Reads an http request and adds data to db.

    Inherit Template from plugin_template.py
    run(socket, address, session) called by PluginManager
    """

    class Http(Base):
        """Represent http table in db.

        Inherit declarative base class from base.py
        """
        __tablename__ = "http"
        id = Column(Integer, primary_key=True)
        address= Column(String, nullable=False)
        command = Column(String)
        path = Column(String)
        version = Column(String)
        headers = Column(String)
        time = Column(DateTime)
        feature = Column(String)

    class Handler(BaseHTTPRequestHandler):
        """Http request handler.

        Inherit Base HTTPRequestHandler from BaseHTTPServer.
        Handle() is automatically called, which parses request and possibly sends a response.
        do_command() methods send an http response and are automatically called in handle().
        """
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
        self.PORT = 80
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
        """Start http request handler, then call get_record and insert_record.

        param: socket --
        param: address -- http client address
        session: session to communicate with db
        return: bool -- True if data is successfully added to http table, False otherwise
        """
        self.session = session
        request_handler = self.Handler(socket, address,  None)

        record = self.get_record(request_handler)

        self.insert_record(record, session)

    def insert_record(self, record, session):
        try:
            session.add(record)
            session.commit()
            session.close()
            return True
        except Exception:

            logging.exception("http record cannot be added to db " ":Time: " + str(datetime.datetime.now()))
            return False

    def get_record(self, handler):
        address = handler.client_address[0]
        command = handler.command
        path = handler.path
        version = handler.request_version
        headers = str(handler.headers)
        time = self.time_stamp
        feature = self.get_feature(address)

        record = self.Http(address=address, command=command, path=path, version=version,
                           headers=headers, time=time, feature=feature)
        return record
