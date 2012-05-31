from config import *
from sqlalchemy import Column, String, Integer, DateTime
#from sqlalchemy.orm import relation
#from sqlalchemy.orm.session import sessionmaker
#from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from unittest import TestCase, main
#from sqlalchemy import create_engine



class Crawl(DeclarativeBase):
    __tablename__ = "Crawl"
    __table_args__ = {'sqlite_autoincrement': True}
    crawlId = Column(Integer(), primary_key=True)
    agentId = Column(Integer(), nullable=False, index=True) #MAC address can be used
    beginDateTime = Column(DateTime(), nullable=True)
    endDateTime = Column(DateTime(), nullable=True)
    userName = Column(String(), nullable=False)
    userDomain = Column(String(), nullable=False)
    nProcessedItems = Column(Integer(), nullable=False)
    nProcessedBytes = Column(Integer(), nullable=False)
    
    def __init__(self, email_style_user_identifier=None):
        from uuid import getnode
        self.agentId = getnode()
        if email_style_user_identifier is None:
            self._setUserByEnvironment()
        else:
            self._setUserByEmail(email_style_user_identifier)
        self.nProcessedBytes = 0
        self.nProcessedItems = 0
    
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
        self.beginDateTime = datetime.now()
    
    def end(self):
        self.endDateTime = datetime.now()
        
    @classmethod
    def dropTable(cls):
        try:
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            print (table)
            table.drop(engine, checkfirst=True)
        except:
            pass
        
    @classmethod
    def createTable(cls):
        try:
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            table.create(engine, checkfirst=True)
        except Exception, e:
            print (e.message)
            pass
        
    def increment(self, processed_bytes):
        self.nProcessedBytes += processed_bytes
        self.nProcessedItems += 1
        
    def getNumberOfProcessedBytes(self):
        return self.nProcessedBytes
    
    def getNumberOfProcessedItems(self):
        return self.nProcessedItems
    
    def getElapsedSeconds(self):
        now = datetime.now()
        elapsed = now - self.beginDateTime
        assert isinstance(elapsed, timedelta)
        return elapsed.total_seconds()
    
    def getFilesPerSecond(self):
        return self.getNumberOfProcessedItems() / self.getElapsedSeconds()
    
    def getBytesPerSecond(self):
        return self.getNumberOfProcessedBytes() / self.getElapsedSeconds()

class _Test(TestCase):
    def setUp(self):
        #DeclarativeBase.metadata.create_all(engine)
        Crawl.dropTable()
        Crawl.createTable()
        self.session = Session()
    
    def testAutoIncrement(self):
        my_crawl_1 = Crawl()
        self.session.add(my_crawl_1)
        my_crawl_2 = Crawl()
        self.session.add(my_crawl_2)
        self.session.commit()
        self.assertEqual(my_crawl_1.crawlId + 1, my_crawl_2.crawlId)

if __name__ == "__main__":
    main()
