from __future__ import unicode_literals, print_function
from MyObject import MyObject, MyCrawl
import os.path
import json
import socket  
from datetime import datetime
from hashlib import sha1
from threading import Thread
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from time import sleep
import locale

def _getHostName():
    try:
        host_name = socket.gethostname()
        assert host_name is not None  
    except:
        host_name = None
    return host_name

class FileInfo(object):
    __stats__ = ["st_size", "st_mtime", "st_ctime", "absolutePath", "gitBlobHash", "host"]
    
    def __str__(self):
        s = "<FileInfo(%s,%s,%s,%s)>" % (self.absolutePath, self.st_size, self.st_mtime, self.st_ctime, self.gitBlobHash)
        return s

    def __repr__(self):
        return self.toJson()
    
    def toJson(self):
        return json.dumps(self.__dict__)

BUFFER_SIZE = 1024 * 1024

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

class GitBlobHash(Thread):
    
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
    def __init__(self, path, sqlalchemy_session):
        Thread.__init__(self)
        self.path = path
        self.sqlAlchemySession = sqlalchemy_session
        self.hostName = _getHostName()
        self.myCrawl = MyCrawl()
    
    def run(self):
        self.myCrawl.begin()
        for root, dirs, files in os.walk(self.path):
            for f in files:
                p = root + os.path.sep + f
                s = os.stat(p)
                git_blob_hash = GitBlobHash(p, s)
                git_blob_hash.start()
                ap = os.path.abspath(p)
                file_info = FileInfo()
                file_info.absolutePath = ap
                file_info.st_size = s.st_size
                file_info.st_mtime = s.st_mtime
                file_info.st_ctime = s.st_ctime
                my_object = MyObject()
                my_object.lastModified = datetime.fromtimestamp(file_info.st_mtime) # naive or aware?
                my_object.lastSeen = datetime.now()
                git_blob_hash.join()
                file_info.gitBlobHash = git_blob_hash.getGitBlobHash()
                #print (file_info.toJson())
                if file_info.gitBlobHash is not None:
                    my_object.uri = "git:blob:" + file_info.gitBlobHash
                my_object.url = "file://" + self.hostName + "/" + file_info.absolutePath
                self.sqlAlchemySession.add(my_object)
                self.myCrawl.increment(git_blob_hash.getReadSize())
        self.myCrawl.end()
        
    def getNumberOfProcessedFiles(self):
        return self.myCrawl.getNumberOfProcessedItems()
    
    def getNumberOfProcessedBytes(self):
        return self.myCrawl.getNumberOfProcessedBytes()
    
    def getFilesPerSecond(self):
        return self.myCrawl.getFilesPerSecond()
    
    def getBytesPerSecond(self):
        return self.myCrawl.getBytesPerSecond()
    
    def __str__(self):
        locale.setlocale(locale.LC_ALL, "")
        return "%dsec %s (%s) bytes, %s (%d) files" % (self.myCrawl.getElapsedSeconds(),
                                                          locale.format("%d", self.getNumberOfProcessedBytes(), grouping=True),
                                                          locale.format("%d", self.getBytesPerSecond(), grouping=True),
                                                          locale.format("%d", self.getNumberOfProcessedFiles(), grouping=True),
                                                          self.getFilesPerSecond())

class _Test(TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///test3.sqlite", echo=True)
        SessionClass = sessionmaker(bind=engine)
        self.session = SessionClass()
    
    def test1(self):
        file_crawler = FileCrawler("C://", self.session)
        file_crawler.start()
        while True:
            file_crawler.join(1)
            if not file_crawler.isAlive(): break
            print(file_crawler)
