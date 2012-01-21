# -*- coding: utf-8 -*- 
'''
@author: Takashi SASAKI
@contact: http://twitter.com/TakashiSasaki

'''
from google.appengine.ext.db import URLProperty, StringListProperty, \
    ListProperty, BooleanProperty, ReferenceProperty, StringProperty
from google.appengine.api.datastore import Key
from unittest.case import TestCase
from GaeAdopter import Initialize
from libobomb.Uuid import GetBase32Uuid
from libobomb.VersionedItemModel import VersionedItemModel

class IdentifierModel(VersionedItemModel):
    identifierString = ReferenceProperty(required=True)
    locationString = ReferenceProperty(required=True)
    selfDescriptiveWords = StringListProperty()
    circumstancesWords = StringListProperty()
    contentsWords = StringListProperty()
    #children = ListProperty(Key)
    #complete = BooleanProperty()
    
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
