__author__ = 'broken'

from google.appengine.ext import db

dbPutQueue = []

def putQueueToDataStore():
    if len(dbPutQueue) > 0:
        db.put(dbPutQueue)