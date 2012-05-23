from webapp2 import RequestHandler, WSGIApplication
from wsgiref.simple_server import demo_app

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm.session import sessionmaker
metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('fullname', String),
                    Column('password', String))
engine = create_engine("sqlite:///test2.sqlite", echo=True)
metadata.create_all(engine)

class User(object):
    def __init__(self, name, fullname, password):
        """SQLAlchemy dows not require this method"""
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        """SQLAlchemy does not require this method"""
        return "<User('%s','%s','%s')>" % (self.name, self.fullname, self.password)

from sqlalchemy.orm import mapper
mapper(User, users_table)

ed_user = User('ed', "Ed Jones", "edpassword")
print (ed_user.fullname)
print (ed_user.id)

Session = sessionmaker(bind=engine)
session = Session()
session.add(ed_user)
session.commit()

class MyHandler(RequestHandler):
    def get(self):
        import os
        self.response.out.write(os.environ)

class MyApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/", MyHandler)])

from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser
from paste.fileapp import FileApp
from paste.evalexception.middleware import EvalException
import paste.translogger
def MyApp2():
    urlMap = URLMap()
    urlMap["/"] = MyApp()
    urlMap["/static"] = StaticURLParser("static")
    urlMap["/favicon.ico"] = FileApp("static/favicon.ico")
    evalException = EvalException(urlMap)
    f = ('[%(time)s] "%(REQUEST_METHOD)s '
              '%(REQUEST_URI)s %(HTTP_VERSION)s" '
              '%(status)s %(bytes)s')
    app = paste.translogger.make_filter(evalException, {}, format=f)
    return app

import webbrowser
if __name__ == "__main__":
    from main import PasteThread
    PasteThread(MyApp(), 10523).start()
    webbrowser.open("http://localhost:10523/", autoraise=1)
