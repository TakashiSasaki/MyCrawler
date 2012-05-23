from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, MetaData, create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.exc import IntegrityError
metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)

class MyObject(DeclarativeBase):
    __tablename__ = "MyObject"
    id = Column(Integer, primary_key=True) #unique only on this database
    sessionId = Column(Integer) #identical for one session
    uri = Column(String())
    url = Column(String())
    size = Column(Integer(), nullable=True)
    lastModified = Column(Date()) #last modified datetime
    lastSeen = Column(Date()) #last seen datetime
    jsonString = Column(String()) #serialized data
    belongsTo = Column(Integer)
    memo0 = Column(String(), nullable=True)
    memo1 = Column(String(), nullable=True)
    memo2 = Column(String(), nullable=True)
    memo3 = Column(String(), nullable=True)
    memo4 = Column(String(), nullable=True)
    memo5 = Column(String(), nullable=True)
    memo6 = Column(String(), nullable=True)
    memo7 = Column(String(), nullable=True)
    memo8 = Column(String(), nullable=True)
    memo9 = Column(String(), nullable=True)

class MemoMap(DeclarativeBase):
    __tablename__ = "MemoMap"
    memoId = Column(Integer, primary_key=True)
    memoName = Column(String(), nullable=False)
    def __init__(self, memo_id, memo_name):
        self.memoId = memo_id
        self.memoName = memo_name
    
class MySession(DeclarativeBase):
    __tablename__ = "Session"
    sessionId = Column(Integer(), primary_key=True)
    agentId = Column(Integer(), nullable=False) #MAC address can be used
    beginDateTime = Column(Date(), nullable=False)
    endDateTime = Column(Date(), nullable=False)
    userName = Column(String(), nullable=False)
    userDomain = Column(String(), nullable=False)

if __name__ == "__main__":
    from uuid import getnode
    node = getnode()
    print (hex(node))
    engine = create_engine("sqlite:///test3.sqlite", echo=True)
    metadata.create_all(engine)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    session.add(MemoMap(2, "two"))
    try:
        session.commit()
    except IntegrityError:
        print ("the row already exists")
    
