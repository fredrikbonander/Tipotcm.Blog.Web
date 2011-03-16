__author__ = 'broken'

from google.appengine.ext import db

class Dictionary(db.Model):
    dict_key = db.StringProperty()

    @property
    def itemId(self):
        return self.key().id()

class DictionaryLabels(db.Model):
    identity = db.StringProperty()
    language = db.StringProperty()
    title = db.StringProperty()

    @property
    def itemId(self):
        return self.key().id()