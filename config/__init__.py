from __future__ import  print_function, unicode_literals
import logging as _logging
_logging.basicConfig(level=_logging.DEBUG)
from logging import debug, info, warn, error, critical, exception
from unittest import TestCase, main
from sqlalchemy import create_engine as _create_engine
engine = _create_engine("sqlite:///test3.sqlite", echo=False)
from sqlalchemy.orm.session import sessionmaker as _sessionmaker
Session = _sessionmaker(bind=engine, autocommit=False)
PersistentSession = _sessionmaker(bind=engine, autocommit=True)
from sqlalchemy import  MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
#_metadata = MetaData()
DeclarativeBase = _declarative_base(metadata=_MetaData())
from datetime import datetime as _datetime
from dateutil.tz import tzutc
def utcnow():
    dt = _datetime.utcnow();
    assert isinstance(dt, _datetime)
    assert dt.tzinfo is None
    dt2 = dt.replace(tzinfo=tzutc())
    return dt2

class _Test(TestCase):
    def setUp(self):
        pass
    
    def testUtcnow(self):
        u = utcnow()
        self.assertIsInstance(u, _datetime, "utcnow() should returns an instance of datetime")
        self.assertIsNotNone(u.tzinfo, "utcnow() should returns aware datetime instance")
        info(u.ctime())
        l = _datetime.now()
        self.assertIsInstance(l, _datetime, "now() should returns an instance off datetime")
        self.assertIsNone(l.tzinfo, "now() should returns native datetime instance")
        info(l.ctime())
