__author__ = 'broken'

COOKIE_KEY = '0f903564-3064-11e0-be1f-c8bcc8dc5f9a'
from gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app