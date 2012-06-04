from config import *
from webapp2 import RequestHandler, WSGIApplication
#from wsgiref.simple_server import demo_app


class _EnvironmentApp(WSGIApplication):
    class _EnvironmentHandler(RequestHandler):
        def get(self):
            import os
            self.response.out.write(os.environ)

    def __init__(self):
        WSGIApplication.__init__(self, [("/Environment", _EnvironmentApp._EnvironmentHandler),
                                        ("/environment", _EnvironmentApp._EnvironmentHandler)],
                                 debug=False, config=None)
        
from api.Record import RecordApp
from api.Crawl import CrawlApp

if __name__ == "__main__":
    from paste.urlparser import StaticURLParser
    html_app = StaticURLParser("html")
    css_app = StaticURLParser("css")
    js_app = StaticURLParser("js")
    
    from paste.cascade import Cascade
    cascaded_app = Cascade([html_app, css_app, js_app, _EnvironmentApp(), RecordApp(), CrawlApp()])
    while True:
        from lib.WsgiRunner import PasteThread
        paste_thread = PasteThread(cascaded_app, 10523, timeout=10)
        info("starting PasteThread")
        paste_thread.start()
        info("waiting for PasteThread to stop")
        paste_thread.join()
        info("restarting PasteThread")
        
    import webbrowser
    webbrowser.open("http://localhost:10523/Record.html", autoraise=1)

class _Test(TestCase):
    crawlAppPort = 20010
    
    def setUp(self):
        from lib.WsgiRunner import PasteThread
        self.pasteThread = PasteThread(CrawlApp(), self.crawlAppPort, timeout=5)
        self.pasteThread.start()
        self.assertTrue(self.pasteThread.isAlive())
        import time
        time.sleep(1)
        
    def test(self):
        from httplib import HTTPConnection
        http_connection = HTTPConnection("localhost", port=self.crawlAppPort)
        http_connection.request('GET', "/api/Crawl")
        response = http_connection.getresponse()
        info(response.status)
        info(response.read())
    
    def tearDown(self):
        info("shutting down")
        self.pasteThread.shutdown()
        info("joining")
        self.pasteThread.join()
