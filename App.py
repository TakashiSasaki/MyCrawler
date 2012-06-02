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

if __name__ == "__main__":
    from paste.urlparser import StaticURLParser
    html_app = StaticURLParser("html")
    css_app = StaticURLParser("css")
    js_app = StaticURLParser("js")
    
    from paste.cascade import Cascade
    cascaded_app = Cascade([html_app, css_app, js_app, _EnvironmentApp(), RecordApp()])
    from lib.WsgiRunner import PasteThread
    PasteThread(cascaded_app, 10523, timeout=10).start()

    import webbrowser
    webbrowser.open("http://localhost:10523/Record.html", autoraise=1)
