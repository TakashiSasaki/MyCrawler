'''
@author: Takashi SASAKI
@contact: http://twitter.com/TakashiSasaki
'''
from google.appengine.ext.db import URLProperty, StringListProperty, \
    ListProperty, BooleanProperty, ReferenceProperty
from google.appengine.api.datastore import Key
from unittest.case import TestCase
from libobomb.SyncModel import SyncModel

class Identifier(SyncModel):
    identifierUri = URLProperty()
    locationUri = URLProperty()
    circumstancesKeywords = StringListProperty()
    contentsKeywords = StringListProperty()
    children = ListProperty(Key)
    complete = BooleanProperty()

class Containment(SyncModel):
    parentIdentifier = ReferenceProperty(Identifier)
    childrenIdentifiers = ListProperty(Key)
    completeness = BooleanProperty()

class Test(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        TestCase.tearDown(self)
    
    def testSomething(self):
        pass
