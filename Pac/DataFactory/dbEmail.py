__author__ = 'broken'

from google.appengine.ext import db

class Email(db.Model):
    name = db.StringProperty()
    language = db.StringProperty()
    content = db.TextProperty()
  