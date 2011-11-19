"""classes in this module are obsolteted."""

from google.appengine.ext import db
from google.appengine.api import users


class DescriptiveMetadataModel(db.Expando):
    """Descriptive metadata describes resource for purposes such as discovery and identification. 
    It can include elements such as title, abstract, author, and keywords. (NISO, ISBN 1-880124-62-9)
    In obomb, this model is indented to hold most generic information.
    They are self descriptive, independent from environment and media.
    """
    idnumber = db.IntegerProperty()
    title = db.StringProperty()
    keywords = db.StringListProperty()
    authors = db.StringListProperty()


class TechnicalMetadataModel(db.Expando): 
    """Technical metadata focuses on how a digital object was created, its format, 
    format-specific technical characteristics, storage and location, etc. 
    Accurate technical metadata helps a repository manage digital 
    objects over time and keep them usable. 
    (http://hul.harvard.edu/ois/digproj/metadata-standards.html)
    """
    idnumber = db.IntegerProperty()
    messageDigest = db.StringProperty()
    size = db.IntegerProperty()
    owner = db.StringProperty()
    createdDateTime = db.DateTimeProperty()
    modifiedDateTime = db.DateTimeProperty()    
    url = db.URLProperty()
    geo = db.GeoPtProperty()

class AdministrativeMetadataModel(db.Expando):
    idnumber = db.IntegerProperty()
    controlledBy = db.UserProperty()
    lastSeenDateTime = db.DateTimeProperty()
    lastSeenBy = db.StringProperty()
    lastSeenFrom = db.StringProperty()
    incomingToken = db.StringProperty()
    outgoingToken = db.StringProperty()
    allowedUsers = db.ListProperty(users.User)

class StructuralMetadataModel(db.Expando):
    """Structural metadata indicates how compound objects are pot together,
    for example, how pages are ordered to form chapters. (NISO ISBN 1-880124-62-9)
    METS (Metadata Encoding & Transmission Standard) includes structural metadata standard.
    """
    idnumber = db.IntegerProperty()
