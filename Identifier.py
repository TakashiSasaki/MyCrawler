# -*- coding: utf-8 -*- 
'''
@author: Takashi SASAKI
@contact: http://twitter.com/TakashiSasaki

'''
from datetime import datetime 
from google.appengine.ext.db import URLProperty, StringListProperty, \
    ListProperty, BooleanProperty, ReferenceProperty, StringProperty
from google.appengine.api.datastore import Key
from GaeAdopter import Initialize
from libobomb.Uuid import GetBase32Uuid
from unittest.case import TestCase
from libobomb.VersionedItem import VersionedItemPolyModel
from libobomb.User import ObombUserModel

class IdentifierModel(VersionedItemPolyModel):
    identifierString = StringProperty(required=True)
    locationString = StringProperty(required=True)
    selfDescriptiveWords = StringListProperty()
    circumstancesWords = StringListProperty()
    contentsWords = StringListProperty()
    #children = ListProperty(Key)
    #complete = BooleanProperty()
    
class ContainmentModel(VersionedItemPolyModel):
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
        owner = ObombUserModel(displayName="TestUser", email="testuser@example.com", lastAccessTime=datetime.now(), deleted=False)
        owner.put()
        Initialize("obomb")
        identifier = IdentifierModel(lockBegins=datetime.now(), lockEnds=datetime.now(), identifierString="urn:uuid:" + GetBase32Uuid(), owner=owner, versionNumber=1111, locationString="http://exmaple.com/a/b/c")
        identifier.circumstancesKeywords = ["いちご", "メロン"]
        identifier.contentsKeywords = ["動物", "植物"]
        identifier.put()
        gql = IdentifierModel.gql("")
        for x in gql.fetch(100):
            assert isinstance(x, IdentifierModel)
            print x
