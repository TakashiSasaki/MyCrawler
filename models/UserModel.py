'''
Created on 2012/01/03

@author: Takashi
'''
from google.appengine.ext import db
class UserModel(db.Model):
    #__slot__ = ["googleUserIdentifier", "mixiUserIdentifier", "twitterUserIdentifier", "YahooJapanUserIdentifier"]
    googleUserIdentifier = db.StringProperty()
    twitterUserIdentifier = db.StringProperty()
    yahooJapanIdentifier = db.StringProperty()
    mixiUserIdentifier = db.StringProperty()
