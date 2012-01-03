'''
Created on 2012/01/03

@author: Takashi
'''
from google.appengine.ext import db
import UserModel
class SessionModel(db.Model):
    sessionIdentifier = db.StringProperty()
    userReference = db.ReferenceProperty(UserModel.UserModel)

SESSION_ID_KEY = "obomb_web_session_key"
