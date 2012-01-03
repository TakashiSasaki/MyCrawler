'''
Created on 2012/01/03

@author: Takashi
'''
from google.appengine.ext import db
class ObombUserKind(db.Model):
    """Obomb user is identified by email and can be bound with accounts on other services."""
    #__slot__ = ["googleUserIdentifier", "mixiUserIdentifier", "twitterUserIdentifier", "YahooJapanUserIdentifier"]
    googleUserIdentifier = db.StringProperty()
    twitterUserIdentifier = db.StringProperty()
    yahooJapanIdentifier = db.StringProperty()
    mixiUserIdentifier = db.StringProperty()
