'''
Created on 2012/01/03

@author: Takashi
'''
import uuid, os, logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from models import SessionKind
from urllib import urlencode
import logging
import login.credentials
from google.appengine.ext.webapp import template

class LoginTwitterRequestHandler(webapp.RequestHandler):
    def get(self):
        current_session = get_current_session()
        if current_session.get(SessionKind.SESSION_ID_KEY) is None:
            current_session[SessionKind.SESSION_ID_KEY] = uuid.uuid1().get_hex()
        session_id = current_session.get(SessionKind.SESSION_ID_KEY)
        
        session_kind_gql = SessionKind.SessionKind.gql("WHERE sessionId = :1", [session_id])
        session_entity = session_kind_gql.get()
        if session_entity is not None:
            session_entity = SessionKind()
            session_entity.sessionId = session_id
            session_entity.put()
            
        if current_session.get("twitter_authorizing") is True:
            access_token = self.request.get("oauth_access_token")
            template_values = {
                'session_id' : current_session.get(SessionKind.SESSION_ID_KEY),
                'access_token' : access_token 
                }
            path = os.path.join(os.path.dirname(__file__), 'twitter.djhtml')
            self.response.out.write(template.render(path, template_values))
            return
        else:
            current_session["twitter_authorizing"] = True
            self.redirect("https://oauth.twitter.com/2/authorize?" + urlencode([("oauth_callback_url", "https://obomb-web.appspot.com/login/twitter"),
                                     ("oauth_mode", "flow_web_client"),
                                     ("oauth_client_identifier", login.credentials.TWITTER_CONSUMER_KEY)]))
            return

    
    def post(self):
        self.get()

if __name__ == "__main__":
    application = webapp.WSGIApplication(
                                     [('/login/twitter', LoginTwitterRequestHandler)],
                                     debug=True)
    run_wsgi_app(application)
