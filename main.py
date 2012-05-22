'''
Created on 2012/05/22

@author: sasaki
'''
from __future__ import  print_function, unicode_literals
from wsgiref.simple_server import demo_app
from threading import Thread

class WsgirefThread(Thread):
    def __init__(self, app=demo_app, port=8001):
        Thread.__init__(self)
        self.app = app
        self.port = port
        if isinstance(app, object):
            self.name = app.__class__.__name__
        else:
            self.name = app.__name__
        
    def run(self):
        print ("running " + self.name + " by wsgiref on localhost:" + str(self.app))
        from wsgiref.simple_server import make_server
        httpd = make_server('', self.port, self.app)
        httpd.serve_forever()
    
class PasteThread(Thread):
    def __init__(self, app=demo_app, port=8002):
        Thread.__init__(self)
        self.app = app
        self.port = port
        if isinstance(app, object):
            self.name = app.__class__.__name__
        else:
            self.name = app.__name__
        
    def run(self):
        print ("running " + self.name + " by paste on localhost:" + str(self.app))
        from paste import httpserver
        httpserver.serve(self.app, host='127.0.0.1', port=str(self.port))

import webbrowser

if __name__ == "__main__":
    WsgirefThread().start()
    PasteThread().start()
    
    import myapp
    WsgirefThread(myapp.MyApp(), 8003).start()
    PasteThread(myapp.MyApp(), 8004).start()
    WsgirefThread(myapp.MyApp2(), 8005).start()
    PasteThread(myapp.MyApp2(), 8006).start()
    webbrowser.open("http://localhost:8001/", autoraise=1)
