# -*- coding: utf-8 -*- 
'''
@author: Takashi SASAKI
@contact: http://twitter.com/TakashiSasaki

'''
from google.appengine.ext.db import URLProperty, StringListProperty, \
    ListProperty, BooleanProperty, ReferenceProperty, StringProperty, Model
from google.appengine.api.datastore import Key
from unittest.case import TestCase
from GaeAdopter import Initialize
from libobomb.Uuid import GetBase32Uuid
from google.appengine.ext.db.polymodel import PolyModel
from libobomb.VersionedItemModel import VersionedItemModel
import logging

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

class IdentifierModel(VersionedItemModel):
    identifierString = StringProperty(required=True)
    timeSpacePoints = ListProperty(Key,required=True)
    labels = ReferenceProperty(LabelsModel)
    circumstances = ListProperty(Key)
    contents = ListProperty(Key)
    #children = ListProperty(Key)
    #complete = BooleanProperty()
    def setCircumstances(self, circumstances_):
        pass
    
class ContainmentModel(VersionedItemModel):
    parentIdentifier = ReferenceProperty(IdentifierModel)
    childrenIdentifiers = ListProperty(Key)
    completeness = BooleanProperty()

class Test(TestCase):
    def setUp(self):
        import logging
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        TestCase.tearDown(self)
    
    def testSomething(self):
        Initialize("obomb")
        identifier = IdentifierModel()
        identifier.identifierUri = "urn:uuid:" + GetBase32Uuid()
        identifier.locationUri = "file://myhost/foo/bar/hoge.iso"
        identifier.circumstancesKeywords = ["いちご", "メロン"]
        identifier.contentsKeywords = ["動物", "植物"]
        identifier.owner = 100
        identifier.put()
        gql = IdentifierModel.gql("")
        cursor = gql.execute()
        self.logger.debug(cursor.si)
        for x in cursor:
            assert isinstance(x, IdentifierModel)
            print x

    def testClassType(self):
        class A(object):
            pass
        alist = [A(), A(), A()]
        assert IsInstances(alist, A)
        logger = logging.getLogger()
        logger.debug(type(A))
        
if __name__ == "__main__":
    class A(object):
        pass
    print type(A)
    print isinstance(A, type)
    