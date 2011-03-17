__author__ = 'broken'
from google.appengine.api import urlfetch
from django.utils import simplejson as json

from Pac.UI import ContentModules
from Pac.UI import PageModules
from Pac.UI import TemplateModules
from Pac.UI import Blog
from Pac.UI import Pages
from Pac import ImageStore
from Pac import Settings

class BaseTemplate():
    def __init__(self, **kwargs):
        # Get page from kwargs
        page = kwargs['page']
        # Set reference to page.key()
        pageKey = page.key()
        # Get pageModules associated with page
        pageModuleList = PageModules.getByPageKey(pageKey)
        pageData = {}
        pageModules = {}
        # Set up pageModules dict with lang as keys
        for market in Settings.markets:
            pageModules[market['language']] = {}

        for pageModule in pageModuleList:
            pageModules[pageModule.lang] = pageModule
            # All content data in store in dbContentModules.ContentModules and not in the pageModules them self
            # Get dbContentModules.ContentModules for pageModule
            pageData[pageModule.lang] = ContentModules.getByPageModuleKey(pageModule.key())

        # Store all data
        self.pageModules = pageModules
        self.pageKey = pageKey
        self.pageData = self.parsePageData(pageData)
        self.modules = []

    def parsePageData(self, data):
        dataAsDict = {}
        if data:
            # Split data between lang dicts
            for lang in data:
                dataAsDict[lang] = {}
                for entry in data[lang]:
                    if entry.content is None:
                        dataAsDict[lang][entry.name] = ''
                    else:
                        dataAsDict[lang][entry.name] = entry.content

        return dataAsDict

    def addModules(self):
        pass

    def preRender(self, query):
        pass
    
    def postRender(self, language, query):
        pass

    def postCache(self, language, query):
        pass

    def renderEditPage(self, query):
        self.addModules()
        self.preRender(query)

class StandardPage(BaseTemplate):
    # Display name in EDIT/new page
    templateName = 'StandardPage'
    #Template to use for main view
    templateFile = 'standardpage.html'

    def __init__(self, **kwargs):
        BaseTemplate.__init__(self, **kwargs)

    def postRender(self, language, query):
        if language in self.pageData and 'MainImage' in self.pageData[language] and self.pageData[language]['MainImage'] != '':
            self.pageData[language]['LeftImage'] = ImageStore.getImageWithDescription(self.pageData[language]['MainImage'], language)

    def addModules(self):
        self.modules.append(TemplateModules.getStandardHeading(self, 'MainHeading'))
        self.modules.append(TemplateModules.getStandardTextBox(self, 'MainTextBox'))
        self.modules.append(TemplateModules.getSingleImageModule(self, 'MainImage'))

class StartPage(BaseTemplate):
    # Display name in EDIT/new page
    templateName = 'StartPage'
    #Template to use for main view
    templateFile = 'startpage.html'

    def postRender(self, language, query):
        if language in self.pageData and 'MainImage' in self.pageData[language] and self.pageData[language]['MainImage'] != '':
            self.pageData[language]['StartPageImage'] = ImageStore.getImageWithDescription(self.pageData[language]['MainImage'], language)

    def addModules(self):
        self.modules.append(TemplateModules.getStandardHeading(self, 'MainHeading'))
        self.modules.append(TemplateModules.getStandardTextBox(self, 'MainTextBox'))
        self.modules.append(TemplateModules.getStandardTextBox(self, 'CopyrightTextBox'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'MetaKeywords'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'MetaDescription'))

class ContactPage(BaseTemplate):
    templateName = 'ContactPage'
    templateFile = 'contactpage.html'

    def addModules(self):
        self.modules.append(TemplateModules.getStandardHeading(self, 'MainHeading'))
        self.modules.append(TemplateModules.getStandardTextBox(self, 'MainTextBox'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'AboutHeading'))
        self.modules.append(TemplateModules.getStandardTextBox(self, 'AboutTextBox'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'YourNameLabel'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'YourEmailLabel'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'ReferenceLabel'))

class GalleryAlbumPage(BaseTemplate):
    # Display name in EDIT/new page
    templateName = 'GalleryAlbumPage'
    #Template to use for main view
    templateFile = 'galleryalbum.html'

    def postRender(self, language, query):
        galleryPages = Pages.getPagesByStringKey(str(self.pageKey))
        self.childGalleryPages = []
        for page in galleryPages:
            pageModule = PageModules.getByPageKeyAndLanguage(page.key(), language)
            contentModule = ContentModules.getByNameAndPageModuleKey('AlbumThumbnail', pageModule.key())
            image = ImageStore.getImageWithDescription(contentModule.content, language)
            self.childGalleryPages.append(dict(name = pageModule.name, path = pageModule.path, image = image))

class GalleryPage(BaseTemplate):
    # Display name in EDIT/new page
    templateName = 'GalleryPage'
    #Template to use for main view
    templateFile = 'imagegallery.html'

    def postRender(self, language, query):
        if language in self.pageData and 'GalleryImages' in self.pageData[language]:
            self.pageData[language]['AlbumName'] = Pages.getParentPageModuleNameByKeyAndLanguage(self.pageKey, language)
            self.pageData[language]['ImageList'] = ImageStore.getImageListDescriptions(self.pageData[language]['GalleryImages'], language)

    def postCache(self, language, query):
        if query.getvalue('thumbnail') == '1':
            self.pageData[language]['thumbNailView'] = True

        if query.getvalue('imageId'):
            self.pageData[language]['currentImageId'] = str(query.getvalue('imageId'))


    def addModules(self):
        self.modules.append(TemplateModules.getStandardHeading(self, 'NextImage'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'PreviousImage'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'ImageText'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'RegularView'))
        self.modules.append(TemplateModules.getStandardHeading(self, 'ThumbnailView'))
        self.modules.append(TemplateModules.getSingleImageModule(self, 'AlbumThumbnail'))
        self.modules.append(TemplateModules.getMultipleImagesModule(self, 'GalleryImages'))


class BlogPage(BaseTemplate):
    # Display name in EDIT/new page
    templateName = 'BlogPage'
    #Template to use for main view
    templateFile = 'newspage.html'

    def __init__(self, **kwargs):
        # Get page from kwargs
        page = kwargs['page']
        # Set reference to page.key()
        pageKey = page.key()
        # Get pageModules associated with page
        pageModuleList = PageModules.getByPageKey(pageKey)
        pageData = {}
        pageModules = {}
        blogPosts = {}
        # Set up pageModules dict with lang as keys
        for market in Settings.markets:
            pageModules[market['language']] = {}
            blogPosts[market['language']] = []

        for pageModule in pageModuleList:
            pageModules[pageModule.lang] = pageModule
            blogPosts[pageModule.lang] = Blog.getByPageModuleKey(pageModule.key())
            # All content data in store in dbContentModules.ContentModules and not in the pageModules them self
            # Get dbContentModules.ContentModules for pageModule
            pageData[pageModule.lang] = ContentModules.getByPageModuleKey(pageModule.key())

        # Store all data
        self.blogPosts = blogPosts
        self.pageModules = pageModules
        self.pageKey = pageKey
        self.pageData = self.parsePageData(pageData)
        self.modules = []

    def preRender(self, query):
        if query.getvalue('blog_post_id'):
            self.currentBlogPost = Blog.getPostById(query.getvalue('blog_post_id'))
        else:
            self.currentBlogPost = Blog.getLatestBlogPost()

    def postRender(self, language, query):
        if language in self.blogPosts:
            self.blogList = self.blogPosts[language]

    def postCache(self, language, query):
        if query.getvalue('blog_post_id'):
            self.currentBlogPost = Blog.getPostById(query.getvalue('blog_post_id'))
        else:
            self.currentBlogPost = Blog.getLatestBlogPost()

        # Twitter feed
        ## http://api.twitter.com/1/statuses/user_timeline.json?screen_name=noradio
        twitterFeedUrl = "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=fbonander&count=5&include_rts=true"
        result = urlfetch.fetch(url=twitterFeedUrl)
        if result.status_code == 200:
            self.twitterFeed = json.loads(result.content)
            
    def addModules(self):
        self.modules.append(TemplateModules.getStandardHeading(self, 'MainHeading'))


class PageContainer(BaseTemplate):
    templateName = 'PageContainer'

    def __init__(self, **kwargs):
        # Get page from kwargs
        page = kwargs['page']
        # Set reference to page.key()
        self.pageKey = page.key()