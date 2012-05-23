from sqlalchemy import  MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
_metadata = MetaData()
DeclarativeBase = _declarative_base(metadata=_metadata)
