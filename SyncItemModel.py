'''
Created on 2012/01/19

@author: Takashi
'''
from google.appengine.ext.db.polymodel import PolyModel
from google.appengine.ext.db import DateTimeProperty, IntegerProperty, EmailProperty, \
    ReferenceProperty

class SyncItemModel(PolyModel):
    """This class models hub style data synchronizing system.
    idNumber is signed integer.    
    zero indicates invalid ID number.
    negative idNumber indicates local ID number.
    positive idNumber is assigned by obomb web service and globally unique.
    None owner indicates that the instance is well-known and authorized by standards outside.
    """
    itemId = ReferenceProperty(required=True)
    owner = ReferenceProperty(required=True)
    lockBegins = DateTimeProperty(required=True)
    lockEnds = DateTimeProperty(required=True)
    versionNumber = IntegerProperty(required=True)
    #lastUploaded = db.DateTimeProperty()
    #lastDownloaded = db.DateTimeProperty()
    #lastStableDurationBegins = db.DateTimeProperty()
    #lastStableDurationEnds = db.DateTimeProperty()
