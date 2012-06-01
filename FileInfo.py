from config import *
import json
from RecordBase import RecordBase
from sqlalchemy import desc
from Crawl import Crawl
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

class FileRecord(RecordBase):
    __slots__ = ["created"]
    
    def __repr__(self):
        return self.toJson()
    
    def toJson(self):
        return json.dumps(self.__dict__)
    
    def exists(self, agent_id, session, best_before_period_in_second):
        last_file_info = getLastFileInfo(agent_id, self.url, session)
        if last_file_info is None: return False
        assert isinstance(last_file_info, RecordBase)
        if last_file_info.lastSeen +  timedelta(seconds = best_before_period_in_second) >= datetime.now():
            return True
        else:
            return False


def getLastFileInfo(agent_id, url, session):
    #print ("selecting for agentId = %d and url = %s" % (agent_id, url))
    my_object_my_crawl = session.query(RecordBase, Crawl).filter(Crawl.agentId == agent_id).filter_by(url=url).order_by(desc(RecordBase.lastSeen)).first()
    if my_object_my_crawl is None: return None
    assert isinstance(my_object_my_crawl[0], RecordBase)
    assert isinstance(my_object_my_crawl[1], Crawl)
    return my_object_my_crawl[0]

class _Test(TestCase):
    def setUp(self):
        try:
            Crawl.dropTable()
        except OperationalError,e:
            debug(e.message)
        RecordBase.dropTable()
        Crawl.createTable()
        RecordBase.createTable()
        #self.session = Session()
    
    def test(self):
        session = Session()
        crawl = Crawl()
        session.add(crawl)
        session.commit()
        file_info = FileRecord()
        file_info.crawlId = crawl.crawlId
        file_info.url = "abc"
        file_info.lastSeen = datetime.now()
        session.add(file_info)
        session.commit()
        file_info_2 = getLastFileInfo(crawl.agentId, "abc", session)
        debug (file_info_2.crawlId)
        self.assertEqual(file_info_2.crawlId, crawl.crawlId)
        session.close()
        
if __name__ == "__main__":
    main()