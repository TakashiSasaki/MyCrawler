'''
Created on 2012/05/22

@author: sasaki
'''
from __future__ import  print_function, unicode_literals
from wsgiref.simple_server import demo_app
from threading import Thread

class WsgirefThread(Thread):
    def __init__(self, app = demo_app):
        Thread.__init__(self)
        self.app = app
        
    def run(self):
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8001, self.app)
        httpd.serve_forever()
    
class PasteThread(Thread):
    def __init__(self, app = demo_app):
        Thread.__init__(self)
        self.app = app
        
    def run(self):
        from paste import httpserver
        httpserver.serve(self.app, host='127.0.0.1', port='8002')

import webbrowser

if __name__ == "__main__":
    while True:
        print ("1: run demo_app by wsgiref on localhost:8001")
        print ("2: run demo_app by paste on localhost:8001")
        a = raw_input("3: exit >")
        if a == "1":
            import myapp
            t = WsgirefThread(myapp.MyApp())
            t.start()
            webbrowser.open("http://localhost:8001/", autoraise=1)
        elif a == "2":
            t = PasteThread(myapp.MyApp())
            t.start()
            webbrowser.open("http://localhost:8002/", autoraise=1)
        elif a == "3":
            print ("bye")
            exit()