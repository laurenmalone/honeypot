from unittest import TestCase
import HoneypotBase
import time
from base import Base
from sqlalchemy import *
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError


class TestHoneypotBase(TestCase):

    def setUp(self):


        HoneypotBase.read_config()
        HoneypotBase.thread_list = []
        HoneypotBase.plugin_instance_list = []

    def test_num_threads_stopped_using_kill(self):

        print "1"
        self.assertTrue(HoneypotBase.import_plugins())
        HoneypotBase.start_manager_threads()
        time.sleep(0.01)
        HoneypotBase.signal_handler('15', None)
        for i in HoneypotBase.thread_list:
            self.assertFalse(i.is_alive())

    def test_num_threads_stopped_using_ctrlc(self):

        print "2"
        self.assertTrue(HoneypotBase.import_plugins())
        del(HoneypotBase.thread_list[:])
        HoneypotBase.start_manager_threads()
        time.sleep(0.01)
        HoneypotBase.signal_handler('^C2', None)
        for i in HoneypotBase.thread_list:
            self.assertFalse(i.is_alive())

    def test_port_valid(self):

        print"3"
        class Plugin():
            def __init__(self, port):
                self._port = port

            def get_port(self):
                return self._port

        HoneypotBase.plugin_instance_list = [Plugin(80), Plugin(23), Plugin(25)]
        self.assertFalse(HoneypotBase.port_valid(80))
        self.assertFalse(HoneypotBase.port_valid(23))
        self.assertFalse(HoneypotBase.port_valid(25))
        self.assertTrue(HoneypotBase.port_valid(90))
        self.assertTrue(HoneypotBase.port_valid(0))
        self.assertTrue(HoneypotBase.port_valid(10))
        self.assertTrue(HoneypotBase.port_valid(0))
        HoneypotBase.signal_handler('15', None)

    def test_load_plugins(self):
        print "4"
        self.assertTrue(HoneypotBase.import_plugins())
        HoneypotBase.signal_handler('15', None)

    def test_bad_plugins_directory(self):
        print "5"
        HoneypotBase.plugin_directory = '/test_plugins'
        self.assertFalse(HoneypotBase.import_plugins())
        HoneypotBase.signal_handler('15', None)


    def test_create_valid_table(self):
        print"7"
        class Test1(Base):
            """Represent test table in db.

            Inherit declarative base class from base.py
            """
            __tablename__ = 'test1'
            id = Column(Integer, primary_key=True)
            a = Column(String, nullable=False)
            b = Column(String, nullable=False)
            c = Column(String, nullable=False)

        HoneypotBase.create_tables()
        self.assertTrue(HoneypotBase.engine.dialect.has_table(HoneypotBase.engine.connect(), "test1"))

    def test_create_table_that_does_not_extend_base(self):
        print"8"
        class Test2():
            """Represent test table in db.

            Inherit declarative base class from base.py
            """
            __tablename__ = 'test2'
            id = Column(Integer, primary_key=True)
            a = Column(String, nullable=False)
            b = Column(String, nullable=False)
            c = Column(String, nullable=False)

        HoneypotBase.create_tables()
        self.assertFalse(HoneypotBase.engine.dialect.has_table(HoneypotBase.engine.connect(), "test2"))

    def test_create_table_that_does_not_define_tablename(self):
        print"9"

        class Test3(Base):
            """Represent test table in db.

            Inherit declarative base class from base.py
            """
            id = Column(Integer, primary_key=True)
            a = Column(String, nullable=False)
            b = Column(String, nullable=False)
            c = Column(String, nullable=False)
        self.assertRaises(InvalidRequestError, lambda: HoneypotBase.create_tables(), Test3)
        #self.assertRaises(InvalidRequestError, HoneypotBase._create_plugin_tables())
        #self.assertRaises(SQLAlchemyError, HoneypotBase._create_plugin_tables())

    def test_create_table_without_columns(self):
        print"10"

        class Test4(Base):
            """Represent test table in db.

            Inherit declarative base class from base.py
            """
            __tablename__ = 'test4'
            a = Column(String, nullable=False)
            b = Column(String, nullable=False)
            c = Column(String, nullable=False)
        self.assertRaises(InvalidRequestError, lambda: HoneypotBase.create_tables(), Test4)
        #self.assertRaises(InvalidRequestError, HoneypotBase._create_plugin_tables())
        #self.assertRaises(SQLAlchemyError, HoneypotBase._create_plugin_tables())

    def test_add_items_to_plugin_table(self):
        class Test5():
            """Represent test table imn db.

            Inherit declarative base class from base.py
            """


    """# def test_bad_plugin(self):
        pass
     """