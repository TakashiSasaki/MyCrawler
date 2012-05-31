from __future__ import  print_function, unicode_literals
import logging as _logging
_logging.basicConfig(level=_logging.DEBUG)
from unittest import TestCase, main
from sqlalchemy import create_engine as _create_engine
engine = _create_engine("sqlite:///test3.sqlite", echo=True)
