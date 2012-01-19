'''
Created on 2012/01/19

@author: Takashi
'''
from google.appengine.ext.db.polymodel import PolyModel
from google.appengine.ext.db import DateTimeProperty, IntegerProperty, EmailProperty

class SyncModel(PolyModel):
    """This class models hub style data synchronizing system.
    idNumber is signed integer.    
    zero indicates invalid ID number.
    negative idNumber indicates local ID number.
    positive idNumber is assigned by obomb web service and globally unique.
    None owner indicates that the instance is well-known and authorized by standards outside.
    """
    syncId = IntegerProperty()
    owner = EmailProperty()
    lockBegins = DateTimeProperty()
    lockEnds = DateTimeProperty()
    versionNumber = IntegerProperty()
    #lastUploaded = db.DateTimeProperty()
    #lastDownloaded = db.DateTimeProperty()
    #lastStableDurationBegins = db.DateTimeProperty()
    #lastStableDurationEnds = db.DateTimeProperty()
