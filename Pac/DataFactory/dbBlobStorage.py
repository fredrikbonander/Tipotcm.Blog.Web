__author__ = 'broken'

from google.appengine.ext import db

class BlobStorage(db.Model):
    fileName = db.StringProperty()
    fileType = db.StringProperty()
    fileData = db.BlobProperty()

    @property
    def itemId(self):
        return self.key().id()