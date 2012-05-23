from __future__ import unicode_literals, print_function
from MyObject import MyObject
import os
import os.path
import json
from datetime import datetime

def _getHostName():
    try:
        import socket  
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
    f = open(path, "rb")
    from hashlib import sha1
    s = sha1()
    s.update("blob %s\0" % size)
    while True:
        b = f.read(BUFFER_SIZE)
        if len(b) == 0: break
        s.update(b)
    return s.hexdigest()

def crawlUnderTheDirectory(path, session):
    for root, dirs, files in os.walk(path):
        for f in files:
            p = root + os.path.sep + f
            ap = os.path.abspath(p)
            s = os.stat(ap)
            file_info = FileInfo()
            file_info.absolutePath = ap
            file_info.st_size = s.st_size
            file_info.st_mtime = s.st_mtime
            file_info.st_ctime = s.st_ctime
            file_info.gitBlobHash = _calculateGitBlobHash(ap, s.st_size)
            print (file_info.toJson())
            my_object = MyObject()
            my_object.lastModified = datetime.fromtimestamp(file_info.st_mtime) # naive or aware?
            my_object.lastSeen = datetime.now()
            my_object.uri = "git:blob:" + file_info.gitBlobHash
            my_object.url = "file://" + _getHostName() + "/" + file_info.absolutePath
            session.add(my_object)

from unittest import TestCase
class _Test(TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///test3.sqlite", echo=True)
        from sqlalchemy.orm.session import sessionmaker
        SessionClass = sessionmaker(bind=engine)
        self.session = SessionClass()
    
    def test1(self):
        crawlUnderTheDirectory(".", self.session)
        self.session.commit()
