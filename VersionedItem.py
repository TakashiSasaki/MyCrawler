'''
Created on 2012/01/19

@author: Takashi
'''
from google.appengine.ext.db.polymodel import PolyModel
from google.appengine.ext.db import DateTimeProperty, IntegerProperty, EmailProperty, \
    ReferenceProperty, Model, StringProperty, BooleanProperty, ListProperty
from unittest.case import TestCase
import datetime
from GaeAdopter import Initialize
from google.appengine.api.datastore_types import Key

class BoundAccountModel(PolyModel):
    serviceName = StringProperty(required=True)
    loginName = StringProperty(required=True)

class ObombUserModel(Model):
    displayName = StringProperty(required=True)
    email = EmailProperty(required=True)
    email2 = EmailProperty()
    lastAccessTime = DateTimeProperty(required=True)
    deleted = BooleanProperty(required=True)
    boundAccounts = ListProperty(Key)

class VersionedItemPolyModel(PolyModel):
    """This class models hub style data synchronizing system.
    idNumber is signed integer.    
    zero indicates invalid ID number.
    negative idNumber indicates local ID number.
    positive idNumber is assigned by obomb web service and globally unique.
    None owner indicates that the instance is well-known and authorized by standards outside.
    """
    owner = ReferenceProperty(ObombUserModel, required=True)
    lockBegins = DateTimeProperty(required=True)
    lockEnds = DateTimeProperty(required=True)
    versionNumber = IntegerProperty(required=True)
    
    #lastUploaded = db.DateTimeProperty()
    #lastDownloaded = db.DateTimeProperty()
    #lastStableDurationBegins = db.DateTimeProperty()
    #lastStableDurationEnds = db.DateTimeProperty()
class Test(TestCase):
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    def startUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testObombUserModel(self):
        Initialize("obomb")
        gql = ObombUserModel.gql("WHERE displayName = :1", ["TestUser"])
        for x in gql.fetch(1000):
            x.delete()
        self.assertEqual(0, gql.count())
        bound_account = BoundAccountModel(loginName="null", serviceName="Twitter")
        bound_account.put()
        obomb_user = ObombUserModel(displayName="TestUser", email="testuser@example.com", lastAccessTime=datetime.datetime.now(), deleted=False)
        obomb_user.boundAccounts = [bound_account.key()]
        obomb_user.put()     
        self.assertEqual(1, gql.count())
        instance = gql.get()
        instance.delete()
        self.assertEqual(0, gql.count())

    def testVersionedItemPolyModel(self):
        Initialize("obomb")
        obomb_user = ObombUserModel(displayName="TestUser", email="testuser@example.com", lastAccessTime=datetime.datetime.now(), deleted=False)
        obomb_user_key = obomb_user.put()
        gql = VersionedItemPolyModel.gql("WHERE owner = :1", [obomb_user_key])
        self.logger.debug(obomb_user_key.__str__())
        for x in gql.fetch(100):
            x.delete()
        self.assertEqual(0, gql.count())
        versioned_item = VersionedItemPolyModel(owner=obomb_user_key, lockBegins=datetime.datetime.now(), lockEnds=datetime.datetime.now(), versionNumber=12345)
        versioned_item.put()
        self.assertEqual(1, gql.count())
        versioned_item.delete()
        self.assertEqual(0, gql.count())
