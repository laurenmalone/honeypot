from plugin_template import Template
from BaseHTTPServer import BaseHTTPRequestHandler
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import json
import datetime
import logging


class Plugin(Template):
    """Reads an http request, responds to client, and adds data to db.

    Inherit Template from plugin_template.py
    run(socket, address, session) called by PluginManager
    """

    class Http(Base):
        """Represent http table in db.

        Inherit declarative base class from base.py
        """
        __tablename__ = "http"
        id = Column(Integer, primary_key=True)
        ip_address= Column(String, nullable=False)
        command = Column(String)
        path = Column(String)
        version = Column(String)
        headers = Column(String)
        time = Column(DateTime)
        feature = Column(String)

    class Handler(BaseHTTPRequestHandler):
        """Http request handler.

        Inherit Base HTTPRequestHandler from BaseHTTPServer.
        Handle() is automatically called, which parses request and sends an error
        msg if appropriate. do_command() methods send an http 400 response and are
        automatically called in handle().
        """

        def __init__(self, socket, address, server, version):
            BaseHTTPRequestHandler.__init__(self, socket, address, server)
            self.protocol_version = version

        def do_GET(self):
            self.send_error(400, 'Bad Request')

        def do_POST(self):
            self.send_error(400, 'Bad Request')

        def do_OPTIONS(self):
            self.send_error(400, 'Bad Request')

        def do_HEAD(self):
            self.send_error(400, 'Bad Request')

        def do_PUT(self):
             self.send_error(400, 'Bad Request')

        def do_DELETE(self):
            self.send_error(400, 'Bad Request')

        def do_TRACE(self):
            self.send_error(400, 'Bad Request')

        def do_CONNECT(self):
            self.send_error(400, 'Bad Request')

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
                    {"name": "ip_address", "type": "TEXT"},
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

        param: socket -- connection to client
        param: address -- client address
        param: session -- session to communicate with db
        """
        self.time_stamp = datetime.datetime.now()
        request_handler = self.Handler(socket, address,  None, "HTTP/1.0")
        record = self.get_record(request_handler)
        self.insert_record(record, session)
        socket.close()

    def insert_record(self, record, session):
        """Insert item into http table

        param: record -- record being added
        session: session to communicate with db
        return: True if data is successfully added, False otherwise
        Raise exception if data cannot be added
        """
        try:
            session.add(record)
            session.commit()
            session.close()
            return True
        except:

            logging.exception("http record cannot be added to db " ":Time: " + str(datetime.datetime.now()))
            return False

    def get_record(self, handler):
        """Get http request record from handler

        param: handler -- Handler instance that communicates with client
        return: record
        Raise exception if field cannot be found in request
        """
        address = handler.client_address[0]
        try:
            command = handler.command
        except:
            command = ""
        try:
            path = handler.path
        except:
            path = ""
        try:
            version = handler.request_version
        except:
            version = ""
        try:
            headers = str(handler.headers)
        except:
            headers = ""
        time = self.time_stamp
        feature = self.get_feature(address)
        record = self.Http(ip_address=address, command=command, path=path, version=version,
                           headers=headers, time=time, feature=feature)

        return record
