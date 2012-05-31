from config import *
from RecordBase import RecordBase
from Crawl import Crawl
import os.path
import json
import socket  
from datetime import datetime
from hashlib import sha1
from threading import Thread
from time import sleep
from FileInfo import FileRecord
import locale

EXCLUDE_DIRECTORIES = ["$Recycle.Bin"]

def _getHostName():
    try:
        host_name = socket.gethostname()
        assert host_name is not None  
    except:
        host_name = None
    return host_name

BUFFER_SIZE = 1024 * 1024 * 4
BEST_BEFORE_PERIOD_IN_SECOND = 3600

def _calculateGitBlobHash(path, size):
    try:
        f = open(path, "rb")
    except IOError:
        return None
    s = sha1()
    s.update("blob %s\0" % size)
    while True:
        b = f.read(BUFFER_SIZE)
        if len(b) == 0: break
        s.update(b)
    return s.hexdigest()
 
class _GitBlobHash(Thread):
    
    def __init__(self, path, size):
        Thread.__init__(self)
        self.path = path
        self.size = size
        self.readSize = 0

    def run(self):
        try:
            f = open(self.path, "rb")
        except IOError, e :
            self.errorMessage = e.message 
            return
        s = sha1()
        s.update("blob %s\0" % self.size)
        while True:
            try:
                b = f.read(BUFFER_SIZE)
            except IOError, e:
                self.errorMessage = e.message
                return
            if len(b) == 0: break
            s.update(b)
            self.readSize += len(b)
        self.gitBlobHash = s.hexdigest()

    def getErrorMessage(self):
        try:
            return self.errorMessage
        except AttributeError:
            return None
        
    def getGitBlobHash(self):
        try:
            return self.gitBlobHash
        except AttributeError:
            return None
    
    def getReadSize(self):
        return self.readSize

class FileCrawler(Thread):
    def __init__(self, path, sqlalchemy_session, max_files=None):
        Thread.__init__(self)
        self.skipCount = 0
        self.maxFiles = max_files
        self.path = path
        self.sqlAlchemySession = sqlalchemy_session
        self.hostName = _getHostName()
        self.crawl = Crawl()
        self.sqlAlchemySession.add(self.crawl)
        self.sqlAlchemySession.commit()
    
    def run(self):
        self.crawl.begin()
        for root, dirs, files in os.walk(self.path):
            if len(dirs) > 0 and dirs[0] in EXCLUDE_DIRECTORIES: dirs = dirs[1:]
            for f in files:
                path = root + os.path.sep + f
                absolute_path = os.path.abspath(path)
                url = "file://" + self.hostName + "/" + absolute_path
                file_info = FileRecord()
                file_info.url = url
                file_info.crawlId = self.crawl.crawlId
                if file_info.exists(self.crawl.agentId, self.sqlAlchemySession, BEST_BEFORE_PERIOD_IN_SECOND):
                    self.skipCount += 1
                    continue
                stat = os.stat(path)
                git_blob_hash = _GitBlobHash(path, stat)
                git_blob_hash.start()
                file_info.size = stat.st_size
                file_info.created = datetime.fromtimestamp(stat.st_ctime)
                file_info.lastModified = datetime.fromtimestamp(stat.st_mtime) # naive or aware?
                file_info.lastSeen = datetime.now()
                git_blob_hash.join()
                hash_string = git_blob_hash.getGitBlobHash()
                if hash_string is not None:
                    file_info.uri = "git:blob:" + hash_string
                self.sqlAlchemySession.add(file_info)
                self.crawl.increment(git_blob_hash.getReadSize())
            if self.maxFiles and  self.crawl.getNumberOfProcessedItems() >= self.maxFiles: break 
        self.crawl.end()
        self.sqlAlchemySession.commit()
    
    def getNumberOfProcessedFiles(self):
        return self.crawl.getNumberOfProcessedItems()
    
    def getNumberOfProcessedBytes(self):
        return self.crawl.getNumberOfProcessedBytes()
    
    def getFilesPerSecond(self):
        return self.crawl.getFilesPerSecond()
    
    def getBytesPerSecond(self):
        return self.crawl.getBytesPerSecond()
    
    def __str__(self):
        locale.setlocale(locale.LC_ALL, "")
        return "%dsec %s (%s) bytes, %s/%s (%d) files" % (self.crawl.getElapsedSeconds(),
                                                          locale.format("%d", self.getNumberOfProcessedBytes(), grouping=True),
                                                          locale.format("%d", self.getBytesPerSecond(), grouping=True),
                                                          locale.format("%d", self.getNumberOfProcessedFiles(), grouping=True),
                                                          locale.format("%d", self.skipCount, grouping=True),
                                                          self.getFilesPerSecond())

class _Test(TestCase):
    
    def setUp(self):
        self.session = Session()
        RecordBase.createTable()
        Crawl.createTable()
        
    
    def test1(self):
        file_crawler = FileCrawler("C://", self.session, max_files = 10)
        file_crawler.start()
        count = 0
        while count < 3:
            file_crawler.join(1)
            if not file_crawler.isAlive(): break
            print(file_crawler)
            count += 1

if __name__ == "__main__":
    main()
