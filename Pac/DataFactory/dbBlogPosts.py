'''
Created on Sep 15, 2010

@author: broken
'''
from google.appengine.ext import db
from Pac.DataFactory import dbPageModules

class BlogPost(db.Model):
    title = db.StringProperty()
    content = db.TextProperty()
    language = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    pageModuleKey = db.ReferenceProperty(dbPageModules.PageModules)
    
    @property
    def itemId(self):
        return self.key().id()