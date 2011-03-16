from google.appengine.ext import db
from Pac.DataFactory import dbUser
from gaesessions import get_current_session

import md5

__author__ = 'broken'

def addNewUser(username, password, permissionLevel):
    user = dbUser.User()

    m = md5.new()
    m.update(password)

    user.username = username
    user.password = m.hexdigest()
    user.permissionLevel = int(permissionLevel)

    db.put(user)

def addOrUpdate(userStringKey, username, password, permissionLevel):
    if userStringKey == '':
        addNewUser(username, password, permissionLevel)
        message = 'Added new user'
    else:
        user = dbUser.User.get(db.Key(userStringKey))
        m = md5.new()
        m.update(password)

        user.username = username
        user.password = m.hexdigest()
        user.permissionLevel = int(permissionLevel)

        db.put(user)
        message = 'Updated user'

    return dict(status=1, message=message)

def getById(userId):
    return dbUser.User.get_by_id(int(userId))

def getAll():
    return dbUser.User.all()

def getContext():
    session = get_current_session()
    if not session or not session.has_key('user'):
        session = { 'user' : { 'authenticated' : False, 'permissionLevel' : 0 }}

    return session

def doLogin(username, password):
    user = dbUser.User.gql('WHERE username = :username', username = username).get()

    if user is None:
        return { 'status' : -1, 'message' : 'The username or password you provided does not match our records.' }

    m = md5.new()
    m.update(password)
    ## Passwords in dbUser is stored as MD5
    passwordAsMD5 = m.hexdigest()

    ## Match passed password as MD5 with dbUser password
    if user.password != passwordAsMD5:
        return { 'status' : -1, 'message' : 'The username or password you provided does not match our records.' }

    session = get_current_session()
    session['user'] = dict(authenticated=True, permissionLevel=user.permissionLevel)
    # Let's try save a dict
    #session['user_premissionLevel'] = user.premissionLevel

    return { 'status' : 1, 'message' : 'User logged in' }

def doLogout():
    session = get_current_session()
    del session['user']
    #del session['user_premissionLevel']

    return { 'status' : 1, 'message' : 'User logged out' }

def isUserAuthenticated():
    session = get_current_session()
    if session and 'user' in session and session['user']['authenticated'] == True:
        return True
    else:
        return False

def hasPermission(view, lvl_required):
    session = get_current_session()

    if lvl_required <= session['user']['premissionLevel']:
        return True
    else:
        view.statusCode = '-1'
        view.statusMessage = 'You don\'t have access to this page!'
        view.templateFile = 'edit/noaccess.html'
        return False