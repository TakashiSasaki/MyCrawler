from config import *
#from __future__ import unicode_literals, print_function
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.exc import IntegrityError
from datetime import datetime
#from MyCrawlTable import MyCrawlTable
#from MyCrawl import MyCrawl
from Crawl import Crawl
from lib.GvizDataTableMixin import GvizDataTableMixin
from lib.DeclarativeBase import DeclarativeBase

class RecordBase(DeclarativeBase, GvizDataTableMixin):
    __tablename__ = "Record"
    __table_args__ = {'sqlite_autoincrement': True}
    
    objectId = Column(Integer, primary_key=True) #unique only on this database
    def getObjectId(self):
        """objectId is the primary key and automatically set"""
        return self.objectId
    
    crawlId = Column(Integer, ForeignKey('Crawl.crawlId'), index=True) #identical for one session
    myCrawlTable = relation(Crawl)
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
        from urlparse import urlsplit, urlunsplit
        split_uri = urlsplit(uri_, allow_fragments=True)
        assert isinstance(split_uri, tuple)
        unsplit_uri = urlunsplit(split_uri)
        if unsplit_uri != uri_:
            debug(unsplit_uri + " != " + uri_)
            raise Exception("%s != %s " %(unsplit_uri ,uri_))
        self.uri = uri_

    url = Column(String(), index=True)
    def getUrl(self):
        return self.url
    def setUrl(self, url_):
        assert isinstance(url_, str)
        from urlparse import urlparse, ParseResult
        parse_result = urlparse(url_, allow_fragments=True)
        rebuilt_url = parse_result.geturl()
        if rebuilt_url != url_:
            raise Exception("malformed URL: " + url_)
        if parse_result[0] not in ("http", "file", "https", "ftp", "file"):
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
        
    exhaustive = Column(Boolean())
    def getExhaustive(self):
        return self.getCompleted()
    def setExhaustive(self, is_completed):
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
    __slots__ = ()
    
    def setUp(self):
        #self.engine = create_engine("sqlite:///test3.sqlite", echo=True)
        DeclarativeBase.metadata.create_all(engine)
        
    def testInsert(self):
        session = Session()
        session.add(MemoMap(2, "two"))
        try:
            session.commit()
        except IntegrityError:
            debug ("the row already exists")
        session.close()
        
    def testUserIdentifier(self):
        crawl = Crawl("a@b")
        self.assertEqual(crawl.userName, "a", "malformed user name")
        self.assertEqual(crawl.userDomain, "b", "malformed user domain")
    
    def testInsert2(self):
        crawl = Crawl()
        crawl.begin()
        self.assertGreater(len(crawl.userName), 0, "no user name was given")
        self.assertGreater(len(crawl.userDomain), 0, "no user domain was given")
        crawl.end()
        session = Session()
        session.add(crawl)
        session.commit()
        debug("crawlId of inserted record is %s" %(crawl.crawlId))
        session.close()
        Crawl.dropTable()
        
    def testGviz(self):
        info(RecordBase.getGvizSchema())
        record_base = RecordBase()
        record_base.setUrl("http://example.com/")
        session = Session()
        session.add(record_base)
        session.commit()
        data_table = record_base.getGvizDataTable(session)
        session.close()
        debug(data_table.ToJSCode("x"))
        debug(data_table.ToCsv())
        debug(data_table.ToHtml())
        debug(data_table.ToJSon())
        debug(data_table.ToJSonResponse())
        debug(data_table.ToResponse())

if __name__ == "__main__":
    main()
