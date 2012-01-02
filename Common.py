import sys, os, os.path
from GaeAdopter import GaeAdopter

# constants
APP_NAME = "obomb"
DATASTORE_NAME = "obomb.db"
BLOBSTORE_NAME = "obomb.blob"
COVERAGE_NAME = "coverage"

dataStorePath = None
blobStorePath = None
appDataPath = None
coveragePath = None
gaeAdopter = None

def MakeApplicationDirectory():
    appDataPath = GetAppDataPath()
    if os.path.isdir(appDataPath): return 
    if os.path.isfile(appDataPath):
        raise Exception("Can't make application directory")
    os.makedirs(appDataPath, 0600)
    
def GetAppDataPath():
    try:
        appdata_path = os.path.abspath(os.environ["APPDATA"])
        return appdata_path + os.sep +  APP_NAME
    except KeyError:
        pass
    try:
        home_path = os.path.abspath(os.environ["HOME"])
        return home_path + os.sep + APP_NAME
    except KeyError:
        pass
    try:
        user_path = os.path.abspath(os.path.expanduser("~"))
        return user_path + os.sep + APP_NAME
    except KeyError:
        pass
    return os.getcwd() + os.sep + "." + APP_NAME

def Trace(function_name):
    assert appDataPath is not None
    coveragePath = appDataPath + os.sep + COVERAGE_NAME
    import trace
    tracer = trace.Trace()
    tracer.run(function_name)
    results = tracer.results()
    results.write_results(True, coverdir=coveragePath)
    
def InitGaeAdopter():
    assert appDataPath is not None
    dataStorePath = appDataPath + os.sep + DATASTORE_NAME
    blobStorePath = appDataPath + os.sep + BLOBSTORE_NAME
    gaeAdopter = GaeAdopter(APP_NAME, datastore_path=dataStorePath, blobstore_path=blobStorePath)

appDataPath = GetAppDataPath()
MakeApplicationDirectory()
InitGaeAdopter()

def _main():
    print 123
    pass
    
if __name__ == "__main__":
    Trace("_main")
