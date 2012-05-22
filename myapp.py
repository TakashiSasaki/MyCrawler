from webapp2 import RequestHandler, WSGIApplication

class MyHandler(RequestHandler):
    def get(self):
        print("abc")
        self.response.out.write("I'm a WSGI application built on webapp2 framework.")

class MyApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/", MyHandler)])
