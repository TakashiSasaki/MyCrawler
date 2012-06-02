from config import *
from gviz_api import DataTable
from webapp2 import RequestHandler, WSGIApplication
from paste.request import path_info_pop

class _RecordHandler(RequestHandler):
    def get(self):
        self.response.out.write(self.request.path_info)
        pass

class RecordApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/Record/?.*", _RecordHandler)])
        
    def __call__(self, environ, start_response):
        path_info_pop(environ)
        #info("PATH_INFO = " + environ["PATH_INFO"]) 
        return WSGIApplication.__call__(self, environ, start_response)

class _Test(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test(self):
        pass
    
    def tearDown(self):
        TestCase.tearDown(self)
        
if __name__ == "__main__":
    main()
