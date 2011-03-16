from Pac.DataFactory import putQueueToDataStore
from Pac.Views import MainView
from Pac.Views import Edit
from Pac.Controller import Helper
from Pac import Utils

__author__ = 'broken'

class GetHandler:
    def __init__(self, path, **kwargs):
        self.userContext = kwargs['userContext']

    def check_permission(self, **kwargs):
        if self.userContext['user']['authenticated']:
            if self.view.permissionLevel > self.userContext['user']['permissionLevel']:
                _view = getattr(Edit, 'NotAuthorized')
                self.view = _view(query = kwargs['query'])
        else:
            _view = getattr(Edit, 'LoginPage')
            self.view = _view(query = kwargs['query'])

class PostHandler:
    def __init__(self, path, **kwargs):
        request = kwargs['request']

        self.redirect = request.headers['Referer'].split('?')[0]
        action = self.pathList[0]
        result = Helper.ActionFactory(action, request)

        putQueueToDataStore()

        if result.message.has_key('redirect'):
            self.redirect = result.message['redirect']
            self.redirect += '&status=' + str(result.message['status'])  + '&message=' + result.message['message']
        else:
            self.redirect += '?status=' + str(result.message['status'])  + '&message=' + result.message['message']

class EditGetHandler(GetHandler):
    def __init__(self, path, **kwargs):
        GetHandler.__init__(self, path, **kwargs)

        self.pathList = Utils.parsePath(path[1])

        _view = getattr(Edit, self.pathList[-1])
        self.view = _view(path = '/'.join(self.pathList), query = kwargs['query'])

        self.check_permission(**kwargs)
        self.view.toTemplate.userContext = self.userContext
        

class EditPostHandler(PostHandler):
    def __init__(self, path, **kwargs):
        self.pathList = Utils.parsePath(path[1])
        PostHandler.__init__(self, path, **kwargs)

class MainGetHandler(GetHandler):
    def __init__(self, path, **kwargs):
        GetHandler.__init__(self, path, **kwargs)

        self.pathList = Utils.parsePath(path[0])

        self.view = MainView(path = '/'.join(self.pathList), query = kwargs['query'])

class MainPostHandler(PostHandler):
    def __init__(self, path, **kwargs):
        self.pathList = Utils.parsePath(path[0])
        PostHandler.__init__(self, path, **kwargs)