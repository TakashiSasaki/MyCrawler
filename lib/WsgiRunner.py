from config import *
from wsgiref.simple_server import demo_app
from threading import Thread

class WsgirefThread(Thread):
    """wsgiref.simple_server is a WSGI application runner."""
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

class _Watchdog(object):
    def __init__(self, server, limit=5):
        from paste.httpserver import WSGIThreadPoolServer
        assert isinstance(server, WSGIThreadPoolServer)
        self.server = server
        self.limit = limit
        self.count = 0
    
    def getTimeoutHandler(self):
        def timeout_handler():
            threads_state = self.server.thread_pool.track_threads()
            n_busy = len(threads_state["busy"])
            n_hung = len(threads_state["hung"])
            n_dying = len(threads_state["dying"])
            n_zombie = len(threads_state["zombie"])
            debug("count=%d busy=%d hung=%d dying=%d zombie=%d" % (self.count, n_busy, n_hung, n_dying, n_zombie))
            n_not_idle = n_busy + n_dying + n_zombie
            if n_not_idle > 0: 
                self.pat()
                return
            self.count += 1
            if self.limit < self.count:
                info("server will be shut down")
                self.server.server_close()
        return timeout_handler

    def pat(self):
        self.count = 0

        
class PasteThread(Thread):
    """paste.httpserve is a WSGI application runner. """
    def __init__(self, app, port, timeout=5):
        self.timeout = timeout
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
        server = httpserver.serve(self.app, host='127.0.0.1', port=str(self.port),
                         start_loop=False,
                         use_threadpool=True,
                         protocol_version="HTTP/1.1",
                         socket_timeout=5)
        if not hasattr(server, "timeout") or server.timeout is None:
            server.timeout = 1
        if server.timeout != 1:
            warn("server.timeout was changed from %d to 1" % (server.timeout))
            server.timeout = 1
        assert server.timeout == 1
        server.handle_timeout = _Watchdog(server, limit=self.timeout).getTimeoutHandler()
        server.serve_forever()
        info("server_forever finished")

import webbrowser

if __name__ == "__main__":
    #WsgirefThread().start()
    PasteThread(demo_app, 8002).start()
    
    from sandbox import myapp
    #WsgirefThread(myapp.MyApp(), 8003).start()
    PasteThread(myapp.MyApp(), 8004).start()
    #WsgirefThread(myapp.MyApp2(), 8005).start()
    PasteThread(myapp.MyApp2(), 8006).start()
    webbrowser.open("http://localhost:8001/", autoraise=1)
    webbrowser.open("http://localhost:8002/", autoraise=1)
    #webbrowser.open("http://localhost:8003/", autoraise=1)
    webbrowser.open("http://localhost:8004/", autoraise=1)
    #webbrowser.open("http://localhost:8005/", autoraise=1)
    webbrowser.open("http://localhost:8006/", autoraise=1)
