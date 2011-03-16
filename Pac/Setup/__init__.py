__author__ = 'broken'
from google.appengine.ext import webapp
from Pac.DataFactory import dbUser
from Pac import Users

class SetupHandler(webapp.RequestHandler):
    def get(self):
        users = Users.getAll()

        if users.count() > 0:
            self.response.out.write('Captain says no!')
        else:
            addFirstTimeUser()
            self.response.out.write('Captain all hands on deck!')

def addFirstTimeUser():
    users = dbUser.User.all()

    if not users.count():
        Users.addNewUser('admin', 'admin', 3)
