from google.appengine.ext import db

class UrlPrefixedTag(db.Expando):
    word = db.StringProperty
    prefixUrl = db.URLProperty
    time = db.DateTimeProperty
