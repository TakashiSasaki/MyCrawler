from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="obomb_web_gae_sessions_key_98937181609869846319751975105710")
    return app
