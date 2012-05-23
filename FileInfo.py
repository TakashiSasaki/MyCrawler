import json
from MyObject import MyObject
from unittest import TestCase
from sqlalchemy import create_engine, desc
from sqlalchemy.orm.session import sessionmaker
from MyCrawl import MyCrawl
from datetime import datetime, timedelta

class FileInfo(MyObject):
    __slots__ = ["created"]
    
    def __repr__(self):
        return self.toJson()
    
    def toJson(self):
        return json.dumps(self.__dict__)
    
    def exists(self, agent_id, session, best_before_period_in_second):
        last_file_info = getLastFileInfo(agent_id, self.url, session)
        if last_file_info is None: return False
        assert isinstance(last_file_info, MyObject)
        if last_file_info.lastSeen +  timedelta(seconds = best_before_period_in_second) >= datetime.now():
            return True
        else:
            return False


def getLastFileInfo(agent_id, url, session):
    #print ("selecting for agentId = %d and url = %s" % (agent_id, url))
    my_object_my_crawl = session.query(MyObject, MyCrawl).filter(MyCrawl.agentId == agent_id).filter_by(url=url).order_by(desc(MyObject.lastSeen)).first()
    if my_object_my_crawl is None: return None
    assert isinstance(my_object_my_crawl[0], MyObject)
    assert isinstance(my_object_my_crawl[1], MyCrawl)
    return my_object_my_crawl[0]

class _Test(TestCase):
    def setUp(self):
        print ("setup")
        engine = create_engine("sqlite:///test3.sqlite", echo=True)
        MyCrawl.dropTable(engine)
        MyObject.dropTable(engine)
        MyCrawl.createTable(engine)
        MyObject.createTable(engine)
        SessionClass = sessionmaker(bind=engine)
        self.session = SessionClass()
    
    def test(self):
        my_crawl = MyCrawl()
        self.session.add(my_crawl)
        self.session.commit()
        file_info = FileInfo()
        file_info.crawlId = my_crawl.crawlId
        file_info.url = "abc"
        file_info.lastSeen = datetime.now()
        self.session.add(file_info)
        self.session.commit()
        file_info_2 = getLastFileInfo(my_crawl.agentId, "abc", self.session)
        print (file_info_2.crawlId)
        self.assertEqual(file_info_2.crawlId, my_crawl.crawlId)
