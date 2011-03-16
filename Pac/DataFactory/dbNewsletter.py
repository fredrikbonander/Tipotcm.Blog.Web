__author__ = 'broken'

from google.appengine.ext import db

class NewsLetter(db.Model):
    email = db.EmailProperty()
