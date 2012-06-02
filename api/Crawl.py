from config import *
from webapp2 import RequestHandler, WSGIApplication
from paste.request import path_info_pop
from lib.Crawl import Crawl
from sqlalchemy.exc import OperationalError

class _CrawlHandler(RequestHandler):
    def get(self):
        self.response.out.write(self.request.path_info)
        if self.request.path_info == "":
            session = Session()
            try:
                data_table = Crawl.getGvizDataTable(session)
                session.close()
            except OperationalError, e:
                self.response.set_status(404)
                self.response.out.write(e.message)
                return
            self.response.out.write(data_table.ToJSonResponse())

class CrawlApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/api/Crawl/?.*", _CrawlHandler)])
        
    def __call__(self, environ, start_response):
        path_info_pop(environ)
        path_info_pop(environ)
        #info("PATH_INFO = " + environ["PATH_INFO"]) 
        return WSGIApplication.__call__(self, environ, start_response)

class _Test(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test(self):
        app = CrawlApp()
    
    def test2(self):
        session = Session()
        info(Crawl.getGvizDataTable(session))
        session.close()
    
    def tearDown(self):
        TestCase.tearDown(self)
        
if __name__ == "__main__":
    main()
