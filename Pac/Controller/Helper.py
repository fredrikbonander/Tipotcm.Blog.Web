
__author__ = 'broken'

from Pac.UI import Pages
from Pac.UI import PageModules
from Pac.UI import ContentModules
from Pac.UI import Blog
from Pac import Users
from Pac import ImageStore
from Resources import ContactMail

class ActionFactory:
    def __init__(self, action, request):
        func = getattr(self, action)
        self.message = func(request)

    def editViewAddNewPage(self, request):
        return Pages.addNewPage(request.get('page_name'), request.get('page_template'), request.get('page_parent_key'))

    def editViewUpdatePage(self, request):
        message = PageModules.addUpdatePageModule(request.get('page_string_key'), request.get('page_module_name'), request.get('language'), request.get('publish'))
        if message['status'] == 1:
            ContentModules.addUpdateContentModule(message['pageModuleKey'], request)
        return message

    def editViewUpdatePageSettings(self, request):
        message = Pages.updatePageSettings(request.get('page_string_key'), request.get('is_startpage'), request.get('sortindex'))
        return message

    def editViewDeletePage(self, request):
        message = Pages.deletePage(request.get('page_string_key'))
        return message

    def editViewDeleteImage(self, request):
        message = ImageStore.DeleteImage(request.get('image_string_key'))
        return message

    def editViewUpdateBlogPost(self, request):
        message = Blog.updateBlogPost(request.get('page_module_string_key'), request.get('blog_post_string_key'), request.get('language'), request.get('title'), request.get('content'))
        return message

    def editViewLoginUser(self, request):
        message = Users.doLogin(request.get('username'), request.get('password'))
        return message

    def editViewAddUpdateUser(self, request):
        message = Users.addOrUpdate(request.get('user_string_key'), request.get('username'), request.get('password'), request.get('permissionLevel'))
        return message

    def editViewLogOut(self, request):
        message = Users.doLogout()
        return message

    def mainViewSendContactEmail(self, request):
        message = ContactMail.send(request.get('name'), request.get('email'), request.get('reference'))
        return message