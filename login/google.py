'''
Created on 2012/01/03

@author: Takashi SASAKI
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from models import SessionModel
import os, uuid
class LoginGoogle(webapp.RequestHandler):
    def get(self):
        current_session = get_current_session()
        if current_session[SessionModel.SESSION_ID_KEY] is None:
            current_session[SessionModel.SESSION_ID_KEY] = uuid.uuid1().get_hex()
        self.response.out.write("<html><body>")
        self.response.out.write("<p>Currently not implemented</p>")
        self.response.out.write("<p>The session ID is %s</p>" % current_session[SessionModel.SESSION_ID_KEY])
        self.response.out.write("</body></html>")
    
    def post(self):
        self.get()

if __name__ == "__main__":
    application = webapp.WSGIApplication(
                                     [('/login/google', LoginGoogle)],
                                     debug=True)
    run_wsgi_app(application)
