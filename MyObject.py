from __future__ import unicode_literals, print_function
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, MetaData, create_engine, DateTime
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.exc import IntegrityError
metadata = MetaData()
DeclarativeBase = declarative_base(metadata=metadata)

class MyObject(DeclarativeBase):
    __tablename__ = "MyObject"
    __table_args__ = {'sqlite_autoincrement': True}
    objectId = Column(Integer, primary_key=True) #unique only on this database
    sessionId = Column(Integer) #identical for one session
    uri = Column(String())
    url = Column(String())
    size = Column(Integer(), nullable=True)
    lastModified = Column(DateTime()) #last modified datetime
    lastSeen = Column(DateTime()) #last seen datetime
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

    @classmethod
    def dropTable(cls):
        try:
            my_object_table = metadata.tables["MyObject"]
            my_object_table.drop(engine, checkfirst=True)
        except:
            pass

class MemoMap(DeclarativeBase):
    __tablename__ = "MemoMap"
    memoId = Column(Integer, primary_key=True)
    memoName = Column(String(), nullable=False)
    def __init__(self, memo_id, memo_name):
        self.memoId = memo_id
        self.memoName = memo_name
    
class MySession(DeclarativeBase):
    __tablename__ = "MySession"
    __table_args__ = {'sqlite_autoincrement': True}
    sessionId = Column(Integer(), primary_key=True)
    agentId = Column(Integer(), nullable=False) #MAC address can be used
    beginDateTime = Column(DateTime(), nullable=False)
    endDateTime = Column(DateTime(), nullable=False)
    userName = Column(String(), nullable=False)
    userDomain = Column(String(), nullable=False)
    
    def __init__(self, email_style_user_identifier=None):
        from uuid import getnode
        self.agentId = getnode()
        if email_style_user_identifier is None:
            self._setUserByEnvironment()
        else:
            self._setUserByEmail(email_style_user_identifier)
    
    def _setUserByEmail(self, email):
        import re
        p = re.compile("^([^@]+)@([^@]+)$")
        m = p.match(email)
        try:
            user_name = m.group(1)
            user_domain = m.group(2)
            assert user_name is not None
            assert user_domain is not None
            self.userName = user_name
            self.userDomain = user_domain
        except:
            self.userName = None
            self.userDomain = None
        
    def _setUserByEnvironment(self):
        import os
        try:
            user_name = os.environ.get("USERNAME")
            assert user_name is not None
        except:
            user_name = None
        self.userName = user_name
        try:
            import socket  
            host_name = socket.gethostname()
            assert host_name is not None  
        except:
            host_name = None
        self.userDomain = host_name
        
    def begin(self):
        from datetime import datetime
        self.beginDateTime = datetime.now()
    
    def end(self):
        from datetime import datetime
        self.endDateTime = datetime.now()
        
    @classmethod
    def dropTable(cls):
        try:
            my_session_table = metadata.tables["MySession"]
            print (my_session_table)
            my_session_table.drop(engine, checkfirst=True)
        except:
            pass
        

if __name__ == "__main__":
    engine = create_engine("sqlite:///test3.sqlite", echo=True)
    metadata.create_all(engine)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    session.add(MemoMap(2, "two"))
    try:
        session.commit()
    except IntegrityError:
        print ("the row already exists")
    
    my_session = MySession("a@b")
    print (my_session.userName)
    print (my_session.userDomain)

    my_session = MySession()
    my_session.begin()
    print (my_session.userName)
    print (my_session.userDomain)
    my_session.end()
    session = SessionClass()
    session.add(my_session)
    session.commit()
    print (my_session.sessionId)

    MySession.dropTable()
    #MyObject.dropTable()
