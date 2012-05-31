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
    def getObjectId(self):
        """objectId is the primary key and automatically set"""
        return self.objectId
    
    crawlId = Column(Integer, ForeignKey('MyCrawl.crawlId'), index=True) #identical for one session
    myCrawlTable = relation(MyCrawl)
    def getCrawlId(self):
        """crawlId is given for one crawl and is a foreign key of MyCrawl table."""
        return self.crawlId
    def setCrawlId(self, crawl_id):
        assert isinstance(crawl_id , int)
        self.crawlId = crawl_id
    
    uri = Column(String())
    def getUri(self):
        return self.uri
    def setUri(self, uri_):
        assert isinstance(uri_, str)
        from urlparse import urlparse, ParseResult
        parse_result = urlparse(uri_, allow_fragments=True)
        assert isinstance(parse_result, ParseResult)
        rebuilt_uri = parse_result.geturl()
        if rebuilt_uri != uri_:
            raise Exception("malformed URI " + uri_)
        self.uri = uri_

    url = Column(String(), index=True)
    def getUrl(self):
        return self.url
    def setUrl(self, url_):
        assert isinstance(url_, str)
        from urlparse import urlparse, ParseResult
        parse_result = urlparse(url_,allow_fragments=True)
        rebuilt_url = parse_result.geturl()
        if rebuilt_url != url_:
            raise Exception("malformed URL: " + url_)
        if parse_result["scheme"] not in ("http", "file", "https", "ftp"):
            raise Exception("unacceptable scheme for URL: + " + parse_result["scheme"])
        self.url = url_
    
    size = Column(Integer(), nullable=True)
    def getSize(self):
        return self.getSize()
    def setSize(self, size_):
        assert isinstance(size_, long)
        self.size = size_

    lastModified = Column(DateTime()) #last modified datetime
    def getLastModified(self):
        return self.lastModified
    def setLastModified(self, last_modified):
        assert isinstance(last_modified, datetime)
        assert last_modified.tzinfo is not None # avoid naive datetime
        self.lastModified = last_modified
    
    lastSeen = Column(DateTime(), index=True) #last seen datetime
    def getLastSeen(self):
        return self.lastSeen
    def setLastSeen(self, last_seen):
        assert isinstance(last_seen, datetime)
        assert last_seen.tzinfo is not None
        self.lastSeen = last_seen
    
    jsonString = Column(String()) #serialized data
    def getJsonString(self):
        return self.jsonString
    def setJsonString(self, json_string):
        assert isinstance(json_string, str)
        from json import loads, dumps
        x = loads(json_string)
        self.jsonString = dumps(x)
    
    belongsTo = Column(Integer())
    def getBelongsTo(self):
        return self.belongsTo
    def setBelongsTo(self, belongs_to):
        assert isinstance(belongs_to, int)
        self.belongsTo = belongs_to 
        
    completed = Column(Boolean())
    def getCompleted(self):
        return self.getCompleted()
    def setCompleted(self, is_completed):
        assert isinstance(is_completed, bool)
        self.completed = is_completed
    
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
    def dropTable(cls):
        try:
            my_object_table = DeclarativeBase.metadata.tables[cls.__tablename__]
            my_object_table.drop(engine, checkfirst=True)
        except:
            pass
        
    @classmethod
    def createTable(cls):
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
    main()