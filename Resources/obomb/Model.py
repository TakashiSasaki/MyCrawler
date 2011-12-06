from google.appengine.ext import db, blobstore
import google.appengine.ext.db.polymodel

#from multiprocessing.managers import SyncManager
#from google.appengine.api import users

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

class SyncModel(google.appengine.ext.db.polymodel.PolyModel):
    """This class models hub style data synchronizing system.
    idNumber is signed integer.
    zero indicates invalid ID number.
    negative idNumber indicates local ID number.
    positive idNumber is assigned by obomb web service and globally unique.
    None owner indicates that the instance is well-known and authorized by standards outside.
    """
    uuid = db.StringProperty()
    owner = db.UserProperty()
    lockBegins = db.DateTimeProperty()
    lockEnds = db.DateTimeProperty()
    versionNumber = db.IntegerProperty()
    #lastUploaded = db.DateTimeProperty()
    #lastDownloaded = db.DateTimeProperty()
    #lastStableDurationBegins = db.DateTimeProperty()
    #lastStableDurationEnds = db.DateTimeProperty()

class ContentModel(SyncModel):
    """Properties in this model never relies on other information
    except the data that sourceUri points to.
    SHA512 is the best on 64bit machine for now.
    """
    sourceUri = db.ReferenceProperty(IriModel)
    #sha512 = db.ByteStringProperty()
    contentString = db.StringProperty() #up to 500 characters
    contentByteString = db.ByteStringProperty() #Like StringProperty, except the value is not encoded in any way. The bytes are stored literally.
    contentText = db.TextProperty() #can store more than 500 characters. not indexed and cannot be used in filters or sort orders.
    
    #Binary data, as a byte string. This is a subclass of the built-in str type.
    #Blob properties are not indexed, and cannot be used in filters or sort orders.
    #Blob is for binary data, such as images. It takes a str value, 
    #but this value is stored as a byte string and is not encoded as text. 
    #Use a Text instance for large text data.
    contentBlob = db.BlobProperty()

    contentBlobReference = blobstore.BlobReferenceProperty()

class EquivalenceModel(SyncModel):
    """Pivot is a set of verses.
    It represents an abstraction or concept.
    pivotId is primary idNumber that is one of verses list. 
    """
    #equivalenceId = db.IntegerProperty()
    equivalents = db.ListProperty(db.Key) #db.Key refers an instance of ContentModel
    primaryVariant = db.ReferenceProperty(ContentModel, collection_name="primaryvariant_set")
    alphabeticVariant = db.ReferenceProperty(ContentModel, collection_name="alphabeticvariant_set")
    rubyVariant = db.ReferenceProperty(ContentModel, collection_name="rubyvariant_set")

class ExclusionModel(SyncModel):
    #exclusionId = db.IntegerProperty()
    exclusives = db.ListProperty(db.Key) # db.Key refers an instance of EquivalenceModel 
    #parentKnot = db.IntegerProperty()   
    #metadataIris = db.ListProperty(db.Key)
    #verse = db.Reference(VerseModel)
    #idnumber = db.IntegerProperty()
    #identityUri = db.ReferenceProperty(IriModel)
    #controlledBy = db.UserProperty()
    #createdDateTime = db.DateTimeProperty()
    #modifiedDateTime = db.DateTimeProperty()

class PredicationModel(SyncModel):
    """A predication is a pair of two terms."""
    #predicationId = db.IntegerProperty()
    arc = db.ReferenceProperty(ContentModel, collection_name="arc_set")
    node = db.ReferenceProperty(ContentModel, collection_name="node_set")


class MetadataModel(SyncModel):
    """A metadata is a set of predications"""
    #metadataId = db.IntegerProperty()
    predications = db.ListProperty(db.Key) # db.Key refers an instance of PredicationModel

###############################################################################
##################### THE FOLLOWING MODELS ARE OBSOLETED. #####################
###############################################################################

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
        iri_model = IriModel()
        iri_model.originalUrl="http://example.com/test"
        iri_model.hierPart = [""]
        iri_model.query = ""
        iri_model.fragment = ""
        iri_model.put()

    def tearDown(self):
        pass

    def test_dummy(self):
        return True
        pass


