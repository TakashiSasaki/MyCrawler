from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, MetaData, create_engine
metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)

class MyObject(DeclarativeBase):
    __tablename__ = "MyObject"
    id = Column(Integer, primary_key=True) #unique only on this database
    agentId = Column(Integer) #MAC address can be used
    sessionId = Column(Integer) #identical for one session
    gitHash = Column(String()) #git style hash value
    uri = Column(String())
    size = Column(Integer())
    lastModified = Column(Date()) #last modified datetime
    lastSeen = Column(Date()) #last seen datetime
    jsonString = Column(String()) #serialized data
    memo0 = Column(String(),nullable=True)
    memo1 = Column(String(),nullable=True)
    memo2 = Column(String(),nullable=True)
    memo3 = Column(String(),nullable=True)
    memo4 = Column(String(),nullable=True)
    memo5 = Column(String(),nullable=True)
    memo6 = Column(String(),nullable=True)
    memo7 = Column(String(),nullable=True)
    memo8 = Column(String(),nullable=True)
    memo0 = Column(String(),nullable=True)

if __name__ == "__main__":
    from uuid import getnode
    node = getnode()
    print (hex(node))
    engine = create_engine("sqlite:///test3.sqlite", echo=True)
    metadata.create_all(engine)

