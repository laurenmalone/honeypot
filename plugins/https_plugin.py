from plugin_template import Template
from BaseHTTPServer import BaseHTTPRequestHandler
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import json
import datetime
import logging
import ssl
from OpenSSL import crypto
from ConfigParser import SafeConfigParser
from os.path import exists, join
import os


class Plugin(Template):
    """Listens for http request, responds to client, and adds data to db.

    Inherit Template from plugin_template.py
    run(socket, address, session) called by PluginManager
    """

    class Https(Base):
        """Represent http table in db.

        Inherit declarative base class from base.py
        """
        __tablename__ = "https"
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
        self.value = "https"
        self.display = "Https"
        self.PORT = 443
        self.description = ("This plugin uses the https port to listen for attackers. "
                            "It returns a 404 not found error to the client "
                            "and stores the information in a sql database.")

        self.ORM = json.dumps({
            "table": {
                "table_name": "https",
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

    def create_cert(self, cert_file, key_file):

        if os.path.isfile(cert_file) and os.path.isfile(key_file):
            print 'already exist'
            return cert_file, key_file

        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "CO"
        cert.get_subject().L = "Denver"
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        open(join(cert_file), 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(key_file), "w").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        return cert_file, key_file



    def read_config(self, config):
        parser = SafeConfigParser()
        parser.read(config)

        cert = parser.get('https', 'cert')
        key = parser.get('https', 'key')

        return cert, key

    def run(self, socket, address, session):
        """Start http request handler, then call get_record and insert_record.

        param: socket -- connection to client
        param: address -- client address
        param: session -- session to communicate with db
        """

        config = self.read_config('honeypot.ini')
        cert_and_key = self.create_cert(config[0], config[1])

        socket = ssl.wrap_socket(socket, keyfile=cert_and_key[1], certfile=cert_and_key[0], server_side=True)
        self.time_stamp = datetime.datetime.now()
        request_handler = self.Handler(socket, address,  None, "HTTP/1.0")
        record = self.get_record(request_handler)
        self.insert_record(record, session)
        #socket.shutdown(SHUT_RDWR)
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
        record = self.Https(ip_address=address, command=command, path=path, version=version,
                            headers=headers, time=time, feature=feature)

        return record
