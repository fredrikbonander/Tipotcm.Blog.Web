'''
Created on Sep 9, 2010

@author: broken
'''
from google.appengine.ext import db

class Pages(db.Model):
    name = db.StringProperty()
    templateType = db.StringProperty()
    startPage = db.BooleanProperty()
    sortIndex = db.IntegerProperty()
    parentStringKey = db.StringProperty()
    
    @property
    def itemId(self):
        return self.key().id()