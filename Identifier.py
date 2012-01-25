# -*- coding: utf-8 -*- 
'''
@author: Takashi SASAKI
@contact: http://twitter.com/TakashiSasaki

'''
from datetime import datetime 
from google.appengine.ext.db import URLProperty, StringListProperty, \
    ListProperty, BooleanProperty, ReferenceProperty, StringProperty, Model, \
    SelfReferenceProperty
from google.appengine.api.datastore import Key
from GaeAdopter import Initialize
from libobomb.Uuid import GetBase32Uuid
from google.appengine.ext.db.polymodel import PolyModel
from libobomb.VersionedItem import VersionedItemPolyModel
from unittest.case import TestCase
import urllib2
from urllib import pathname2url
from urlparse import urlparse

class WordsModel(PolyModel):
    words = StringListProperty()
    
class LabelsModel(WordsModel):
    pass
    
class CircumstanceModel(WordsModel):
    pass

class ContentModel(WordsModel):
    pass

def IsInstances(list_, class_):
    assert isinstance(list_, list) or isinstance(list_, tuple)
    assert isinstance(class_, type)
    for x in list_:
        if not isinstance(x, class_):
            return False
    return True

class IdentifierModel(VersionedItemPolyModel):
    identifierString = StringProperty(required=True)
    timeSpacePoints = ListProperty(Key, required=True)
    labels = ReferenceProperty(LabelsModel)
    circumstances = ListProperty(Key)
    contents = ListProperty(Key)
    metadata = ListProperty(Key)
    #children = ListProperty(Key)
    #complete = BooleanProperty()
    anchor = SelfReferenceProperty()
    def setCircumstances(self, circumstances_):
        pass

#class ContainmentModel(VersionedItemPolyModel):
#   parentIdentifier = ReferenceProperty(IdentifierModel)
#   childrenIdentifiers = ListProperty(Key)
#    completeness = BooleanProperty()

class Test(TestCase):
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def testSomething(self):
        Initialize("obomb")
        #owner = ObombUserModel(displayName="TestUser", email="testuser@example.com", lastAccessTime=datetime.now(), deleted=False)
        #owner.put()
        Initialize("obomb")
        identifier = IdentifierModel(lockBegins=datetime.now(), lockEnds=datetime.now(), identifierString="urn:uuid:" + GetBase32Uuid(),
                                     owner=22222, versionNumber=1111, locationString="http://exmaple.com/a/b/c"
                                     , item=456)
        identifier.circumstancesKeywords = ["いちご", "メロン"]
        identifier.contentsKeywords = ["動物", "植物"]
        identifier.put()
        gql = IdentifierModel.gql("")
        for x in gql.fetch(100):
            assert isinstance(x, IdentifierModel)
            print x

    def testClassType(self):
        class A(object):
            pass
        alist = [A(), A(), A()]
        assert IsInstances(alist, A)
        self.logger.debug(type(A))
    
    def testTraverse(self):
        import os
        file_counter = 0
        dir_counter = 0
        for root, dirs, files in os.walk(".."):
            for file in files:
                file_counter += 1
                path = os.path.abspath(os.path.join(root, file))
                url = pathname2url(path)
                parsed = urlparse(url)
                self.logger.debug("file[" + str(file_counter) + "]" + parsed.geturl())
                #identifier = IdentifierModel() 
            for dir in dirs:
                dir_counter += 1
                path = os.path.abspath(os.path.join(root, dir))
                url = pathname2url(path)
                parsed = urlparse(url)
        
                self.logger.debug("dir[" + str(dir_counter) + "]" + parsed.geturl())
        
if __name__ == "__main__":
    class A(object):
        pass
    print type(A)
    print isinstance(A, type)
    
