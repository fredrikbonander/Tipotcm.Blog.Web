__author__ = 'broken'
from google.appengine.api import blobstore
from Pac.UI import PageTemplates
from Pac.UI import Pages as PacPages
from Pac.Views import View
from Pac import ImageStore as PacImageStore
from Pac import UI
from Pac import Users

class NotAuthorized(View):
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)

        self.templateFile = 'not_authorized.html'
        self.permissionLevel = 0
        self.isEdit = True

class Dashboard(View):
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)

        self.templateFile = 'dashboard.html'
        self.permissionLevel = 1
        self.isEdit = True
        self.toTemplate.blogPages = PacPages.getBlogPages()

class Pages(View):
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)

        self.templateFile = 'pages.html'
        self.permissionLevel = 1
        self.isEdit = True
        self.toTemplate.pageTree = UI.getPageTreeForEditView()

        query = kwargs['query']
        if query.getvalue('item_id'):
            self.toTemplate.itemId = str(query.getvalue('item_id'))
            self.currentPage = UI.Pages.getById(self.toTemplate.itemId)
            if self.currentPage:
                templateStr = self.currentPage.templateType.split('.')[-1]
                template = getattr(PageTemplates, templateStr)
                self.toTemplate.pageTemplate = template(page = self.currentPage)
                # Add modules for EditView
                self.toTemplate.pageTemplate.renderEditPage(query)

class NewPage(Pages):
    def __init__(self, **kwargs):
        Pages.__init__(self, **kwargs)

        self.templateFile = 'newpage.html'
        self.permissionLevel = 1
        self.isEdit = True
        self.toTemplate.templatesList = UI.getPageTemplates()


class ImageStore(View):
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)

        self.templateFile = 'imagestore.html'
        self.permissionLevel = 1
        self.isEdit = True
        self.toTemplate.uploadUrl = blobstore.create_upload_url('/edit/AddUpdateImageStore')
        self.toTemplate.imageList = PacImageStore.getAll()

        query = kwargs['query']
        if query.getvalue('item_id'):
            self.itemId = str(query.getvalue('item_id'))
            self.toTemplate.currentImage = PacImageStore.getByIdForEdit(self.itemId)

class Settings(Pages):
    def __init__(self, **kwargs):
        Pages.__init__(self, **kwargs)

        self.templateFile = 'settings.html'
        self.permissionLevel = 2
        self.isEdit = True

        query = kwargs['query']
        if query.getvalue('item_id'):
            self.toTemplate.currentUser = Users.getById(query.getvalue('item_id'))

        self.toTemplate.userList = Users.getAll()

class LoginPage(Pages):
    def __init__(self, **kwargs):
        Pages.__init__(self, **kwargs)

        self.templateFile = 'login.html'
        self.permissionLevel = 0
        self.isEdit = True

class Main(Dashboard):
    pass