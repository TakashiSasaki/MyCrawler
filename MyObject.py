from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer
DeclarativeBase = declarative_base()

class MyObject(DeclarativeBase):
    __tablename__ = "MyObject"
    localId = Column(Integer, primary_key = True)
    sessionId= Column(Integer)
    gitHash = Column(String())
    uri = Column(String())
    size = Column(Integer())
    unchangedBegin = Column(Date())
    unchangedLast = Column(Date())
    jsonString = Column(String())

from uuid import getnode
node = getnode()
print (hex(node))