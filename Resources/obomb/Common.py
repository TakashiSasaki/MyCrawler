import sys, os, os.path
from compiler.ast import Pass

class Common(object):
    def __init__(self):
        self.MakeApplicationDirectory()
    
    def MakeApplicationDirectory(self):
        application_directory = self.GetApplicationDirectory()
        if os.path.isdir(application_directory): return 
        if os.path.isfile(application_directory):
            raise Exception("Can't make application directory")
        os.makedirs(application_directory, 0600)
        
    def GetApplicationDirectory(self):
        try:
            appdata_path = os.path.abspath(os.environ["APPDATA"])
            return appdata_path + os.sep +  "obomb"
        except KeyError:
            pass
        try:
            self.home_path = os.path.abspath(os.environ["HOME"])
            return home_path + os.sep + ".obomb"
        except KeyError:
            pass
        try:
            user_path = os.path.abspath(os.path.expanduser("~"))
            return user_path + os.sep + ".obomb"
        except KeyError:
            pass
        return os.getcwd() + os.sep + ".obomb"

if __name__ == "__main__":
    common = Common()
    print common.GetApplicationDirectory()
    common.MakeApplicationDirectory()