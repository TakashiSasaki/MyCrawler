from __future__ import  print_function, unicode_literals
import logging as _logging
_logging.basicConfig(level=_logging.DEBUG)
from unittest import TestCase, main
from sqlalchemy import create_engine as _create_engine
engine = _create_engine("sqlite:///test3.sqlite", echo=True)
from sqlalchemy.orm.session import sessionmaker as _sessionmaker
Session = _sessionmaker(bind=engine)
from sqlalchemy import  MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
#_metadata = MetaData()
DeclarativeBase = _declarative_base(metadata=_MetaData())
