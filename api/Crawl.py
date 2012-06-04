from config import *
from webapp2 import RequestHandler, WSGIApplication
from paste.request import path_info_pop
from lib.Crawl import Crawl
from sqlalchemy.exc import OperationalError

class _CrawlHandler(RequestHandler):
    def get(self):
        self.lastPathInfo = self.request.path_info
        if self.request.path_info == "":
            session = Session()
            try:
                data_table = Crawl.getGvizDataTable(session)
                session.close()
                self.response.out.write(data_table.ToJSonResponse())
                return
            except OperationalError, e:
                self.response.set_status(404)
                self.response.out.write(e.message)
                return

        if self.request.path_info == "/create":
            try:
                Crawl.createTable()
                self.response.set_status(200)
                self.response.out.write("Crawl.createTable")
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return
        
        if self.request.path_info == "/drop":
            try:
                Crawl.dropTable()
                self.response.set_status(200)
                self.response.out.write("Crawl.dropTable")
            except Exception,e :
                self.response.set_status(500)
                self.response.out.write(e.message)
            return
        if self.request.path_info == "/dummy":
            try:
                Crawl.insertDummyRecords()
                self.response.set_status(200)
                self.response.out.write("Crawl.insertDummyRecords")
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return     
            
    def getLastPathInfo(self):
        return self.lastPathIngo

class CrawlApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/api/Crawl/?.*", _CrawlHandler)])
        
    def __call__(self, environ, start_response):
        path_info_pop(environ)
        path_info_pop(environ)
        #info("PATH_INFO = " + environ["PATH_INFO"]) 
        return WSGIApplication.__call__(self, environ, start_response)

class _Test(TestCase):
    port = 20111
    
    def setUp(self):
        TestCase.setUp(self)
        from lib.WsgiRunner import PasteThread
        self.pasteThread = PasteThread(CrawlApp(), self.port, timeout=5)
        self.pasteThread.start()
        import time
        time.sleep(1)
        
    def testGet(self):
        self.assertTrue(self.pasteThread.isAlive())
        from httplib import HTTPConnection
        http_connection = HTTPConnection("localhost", port=self.port)
        http_connection.request("GET", "/api/Crawl")
        response = http_connection.getresponse()
        self.assertTrue(response.status == 404 or response.status == 200)
    
    def test2(self):
        session = Session()
        info(Crawl.getGvizDataTable(session))
        session.close()
    
    def tearDown(self):
        TestCase.tearDown(self)
        
if __name__ == "__main__":
    main()
