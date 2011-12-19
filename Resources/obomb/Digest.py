import io
import hashlib
import base64
from google.appengine.ext import db

class DigestModel(db.Model):
    hashMethod = db.StringProperty()
    hashBase32 = db.StringProperty()
    size = db.IntegerProperty()

class Digest(object):
    __slots__ = ["hashMethod", "hashHex", "hashBase32", "hashBase64", "size", "model"]
    
    def __init__(self):
        pass
    
    def OpenFile(self, file_name):
        buffered_reader = io.open(file_name, "rb")
        assert isinstance(buffered_reader, io.BufferedReader)
        self.size = 0
        self.hashMethod = "sha256"
        sha256 = hashlib.sha256()
        while True:
            r = buffered_reader.read()
            sha256.update(r)
            l = len(r)
            if l == 0: break
            self.size += l
        self.hashBase32 = base64.b32encode(sha256.digest())
        self.hashBase64 = base64.b64encode(sha256.digest())
        self.hashHex = sha256.hexdigest()
        
    def Uri(self):
        return "URN:" + self.hashMethod.upper() + ":" + self.hashBase32
        #return "urn:" + self.hashMethod + ":" + self.hashBase64
        
    def Get(self):
        pass
    
    def Put(self):
        pass

import unittest
class Test(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.tearDown(self)
    
    def testFileIO(self):
        a = io.FileIO("Digest.py")
        assert isinstance(a, io.FileIO)
        a = io.open("Digest.py")
        assert isinstance(a, io.TextIOWrapper)
        a = io.open("Digest.py", "rb")
        assert isinstance(a, io.BufferedReader)
        a = open("Digest.py")
        assert isinstance(a, file)

    def testDigest(self):
        self.digest = Digest()
        self.digest.OpenFile("Digest.py")
        assert self.digest.size > 0
        assert len(self.digest.hashHex) == 64
        assert len(self.digest.hashBase32) == 56
        print  self.digest.GetUri()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
