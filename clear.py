'''
Created on 2012/01/03

@author: Takashi SASAKI
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from models import SessionKind
import os, uuid
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models.ObombUserKind import ObombUserKind

class ClearRequestHandler(webapp.RequestHandler):
    def get(self):
        current_session = get_current_session()
        if current_session.get(SessionKind.SESSION_ID_KEY) is not None:
            current_session.clear()

        template_values = {
            }
        path = os.path.join(os.path.dirname(__file__), 'clear.djhtml')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        self.get()

if __name__ == "__main__":
    application = webapp.WSGIApplication(
                                     [('/clear', ClearRequestHandler)],
                                     debug=True)
    run_wsgi_app(application)
