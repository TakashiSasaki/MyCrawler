from google.appengine.ext import db
from google.appengine.api import users

class IriModel(db.Model):
    """
      URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
      hier-part   = "//" authority path-abempty / path-absolute / path-rootless / path-empty

       foo://example.com:8042/over/there?name=ferret#nose
       \_/   \______________/\_________/ \_________/ \__/
     scheme     authority       path        query   fragment
        |   _____________________|__
       / \ /                        \
       urn:example:animal:ferret:nose
    """
    originalUrl = db.URLProperty()
    hierPart = db.StringListProperty()
    query = db.StringProperty()
    fragment = db.StringProperty()
    
    def SetIri(self):
        """sets uri and its components.
        Each decomposed part will be normalized and decoded.
        Punycode and percent encoded string will be decoded.
        """
         
    def GetHierPart(self):
        """returns list of components in hier-part defined in RFC 3986.
        List includes sub-delim and colon.
        """
        return self.hierPart
        
    def GetQueryPart(self):
        return self.query

    def GetFragment(self):
        return self.fragment

class VerseModel(db.polymodel.PolyModel):
    """Properties in this model never relies on other information
    except the data that sourceUri points to.
    SHA512 is the best on 64bit machine for now.
    """
    sourceUri = db.ReferenceProperty(IriModel)
    sha512 = db.ByteStringProperty()
    retrievedString = db.StringProperty()
    retrievedBlob = db.BlobProperty()
    retrievedText = db.TextProperty()


class SyncModel(VerseModel):
    """This class models hub style data synchronizing system.
    idNumber is signed integer.
    zero indicates invalid ID number.
    negative idNumber indicates local ID number.
    positive idNumber is assigned by obomb web service and globally unique.
	None owner indicates that the instance is well-known and authorized by standards outside.
    """
    idNumber = db.IntegerProperty()
    owner = db.UserProperty()
    lockBegins = db.DateTimeProperty()
    lockEnds = db.DateTimeProperty()
    #lastUploaded = db.DateTimeProperty()
    #lastDownloaded = db.DateTimeProperty()
    #lastStableDurationBegins = db.DateTimeProperty()
    #lastStableDurationEnds = db.DateTimeProperty()

class PivotModel(db.polymodel.PolyModel):
    """Pivot is a set of verses.
    It represents an abstraction or concept.
    pivotId is primary idNumber that is one of verses list. 
    """
    idNumber = db.IntegerProperty()
    verseItems = db.ListProperty(db.IntegerProperty)

class KnotModel(PivotModel):
    parentKnot = db.IntegerProperty()   
    metadataIris = db.ListProperty(db.Key)
    #verse = db.Reference(VerseModel)
    #idnumber = db.IntegerProperty()
    #identityUri = db.ReferenceProperty(IriModel)
    #controlledBy = db.UserProperty()
    #createdDateTime = db.DateTimeProperty()
    #modifiedDateTime = db.DateTimeProperty()

class PredicationModel(db.Model):
    predicationId = db.IntegerProperty()
    arc = db.IntegerProperty()
    node = db.IntegerProperty()

class MetadataModel(db.Model):
    metadataId = db.IntegerProperty()
    predications = db.ListProperty(db.IntegerProperty)

###############################################################################
##################### THE FOLLOWING MODELS ARE OBSOLETED. #####################
###############################################################################

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

#class MetadataSuiteModel(db.Expando):
#    idnumber = db.IntegerProperty()
#    descriptiveMetadata = db.ReferenceProperty(DescriptiveMetadataModel)
#    technicalMetadata = db.ReferenceProperty(TechnicalMetadataModel)
#    administrativeMetadata = db.ReferenceProperty(AdministrativeMetadataModel)
#    structuralMetadata = db.ReferenceProperty(StructuralMetadataModel)
#    knot = db.ReferenceProperty(TagNodeModel)
#    obsoletedBy = db.SelfReference(collection_name="obsoletedBy_set")
#    equivalentTo = db.SelfReference(collection_name="equivalentTo_set")

#    def GetScheme(self):
#        """returns normalized scheme"""
#        scheme = self.scheme
#        r = re.compile("^[a-z0-9+-.]+$")
#        m = r.match(scheme)
#        assert m is not None
#        return scheme
    
#    def GetNonAuthority(self):
#        """returns list of non-authority components defined in RFC3986.
#        List includes sub-delim and colon.
#        """
#        return self.nonAuthority
    
#    def GetHost(self):
#        """returns normlized host if the url has authority part.
#        If original url does not have authority part, it returns None.
#        Since "file:///a.txt" does have zero-length authority part, it returns zero-length string.
#        """
#        host = self.host
#        if self.host is None: return None
#        r = re.compile("^[a-z0-9\.]*$")
#        m = r.match(host)
#        assert m is not None
#        return host
#    
#    def GetPort(self):
#        """returns port by int if the url has authority part with explicit port part.
#        port part could be lost while scheme based url normalization described in RFC3986.
#        """
#        port = self.port
#        assert port is None or isinstance(port, IntType)
#        return port
#    
#    def GetSegments(self):
#        """returns list of segments if the url has hier_part defined in RFC3986.
#        Leading slash of each segment is omitted.
#        Thus zero-length string represents slash itself.
#        """
#        return self.segments

#########################################################################################
########################## THE END OF OBSOLETED MODELS ##################################
#########################################################################################

import unittest
class Test(unittest.TestCase):
    def setUp(self):
        descriptive_metadata = DescriptiveMetadataModel()
        descriptive_metadata.authors = ["Takashi SASAKI", "Nanashi no Gombei"]
        descriptive_metadata.keywords = ["Sunday", "Monday"]
        descriptive_metadata.title = "Sunny day"
        descriptive_metadata.put()

    def tearDown(self):
        pass

    def testName(self):
        pass


