from config import *
#from __future__ import unicode_literals, print_function
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, MetaData, create_engine, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
#from MyCrawlTable import MyCrawlTable
from DeclarativeBase import DeclarativeBase
from MyCrawl import MyCrawl

class MyObject(DeclarativeBase):
    __tablename__ = "MyObject"
    __table_args__ = {'sqlite_autoincrement': True}
    objectId = Column(Integer, primary_key=True) #unique only on this database
    crawlId = Column(Integer, ForeignKey('MyCrawl.crawlId'), index=True) #identical for one session
    myCrawlTable = relation(MyCrawl)
    uri = Column(String())
    url = Column(String(), index=True)
    size = Column(Integer(), nullable=True)
    lastModified = Column(DateTime()) #last modified datetime
    lastSeen = Column(DateTime(), index=True) #last seen datetime
    jsonString = Column(String()) #serialized data
    belongsTo = Column(Integer())
    completed = Column(Boolean())
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

    def __str__(self):
        s = "<MyObject(%s,%s,%s,%s,%s)>" % (self.url, self.size, self.lastModified, self.lastSeen, self.uri)
        return s

    @classmethod
    def dropTable(cls, engine):
        try:
            my_object_table = DeclarativeBase.metadata.tables[cls.__tablename__]
            my_object_table.drop(engine, checkfirst=True)
        except:
            pass
        
    @classmethod
    def createTable(cls, engine):
        try:
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            table.create(engine, checkfirst=True)
        except:
            pass

class MemoMap(DeclarativeBase):
    __tablename__ = "MemoMap"
    memoId = Column(Integer, primary_key=True)
    memoName = Column(String(), nullable=False)
    def __init__(self, memo_id, memo_name):
        self.memoId = memo_id
        self.memoName = memo_name
    
class _Test(TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///test3.sqlite", echo=True)
        DeclarativeBase.metadata.create_all(self.engine)

        SessionClass = sessionmaker(bind=self.engine)
        self.session = SessionClass()
        
    def test1(self):
        self.session.add(MemoMap(2, "two"))
        try:
            self.session.commit()
        except IntegrityError:
            print ("the row already exists")
        
    def test2(self):
        my_session = MyCrawl("a@b")
        print (my_session.userName)
        print (my_session.userDomain)
    
    def test3(self):
        my_session = MyCrawl()
        my_session.begin()
        print (my_session.userName)
        print (my_session.userDomain)
        my_session.end()
        
        #session = SessionClass()
        self.session.add(my_session)
        self.session.commit()
        print (my_session.crawlId)
    
        MyCrawl.dropTable(self.engine)
        #MyObject.dropTable()

if __name__ == "__main__":
    import unittest
    unittest.main()
