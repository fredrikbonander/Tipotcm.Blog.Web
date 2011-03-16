__author__ = 'broken'
from google.appengine.api import memcache
from Pac.UI import PageModules
from Pac.UI import PageTemplates
from Pac import Utils
from Pac import Settings
from Pac import UI

class View:
    def __init__(self, **kwargs):
        query = kwargs['query']

        self.templateFile = ''
        self.permissionLevel = 0
        self.isEdit = False
        self.toTemplate = Utils.dictObj()
        self.toTemplate.markets = Settings.markets

        if 'path' in kwargs:
            self.toTemplate.path = kwargs['path']

        self.toTemplate.currentView = self

        if query.getvalue('status'):
            self.toTemplate.statusCode = query.getvalue('status')
            self.toTemplate.statusMessage = query.getvalue('message')

class MainView(View):
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)

        path = kwargs['path']
        query = kwargs['query']

        self.lang = path.split('/')[0]
        self.path = '/' + path + '/'
        
        self.pageRefresh = False
        # If pagerefresh is present in query with value "true", skip memcache and reload the page from datastore
        if query.getvalue('pagerefresh') == 'true':
            self.pageRefresh = True
            Settings.forceMemcacheRefresh = True

        self.preparePage(query)
        self.renderPage(query)

    def preparePage(self, query):
        # Set up memcacheid based on language
        memcacheid = "mainView_pageTree_%s" % self.lang
        pageTree = memcache.get(memcacheid) #@UndefinedVariable
        # If pageTree is not in memcache, build pageTree and store it in memcache
        if pageTree is None or self.pageRefresh:
            pageTree = UI.getPageTreeForMainView(self.lang, memcacheid)

        # Set currentPage to None as a precaution
        self.toTemplate.currentPage = None
        # Bind pageTree to view
        self.toTemplate.pageTree = pageTree
        #How to get pagecontainer items
        self.toTemplate.footerPageTree = UI.getFooterPageTree(self.lang)
        #footerPageContainer = dbPages.Pages.get_by_key_name('footermenu')
        #if footerPageContainer:
        #    footerPages = dbPages.Pages.gql('WHERE parentKey = :parentKey', parentKey = footerPageContainer.key()).fetch(100)
        #    view.footerTree = PageService.build_tree(footerPages, pageRoot = footerPageContainer, pageModules = pageModules)[0]

        # Get path to special pages

        # Bind pages to view
        #view.pages = pages

    def renderPage(self, query):
        # If we are at root page in URL
        if self.path == '/' + self.lang + '/':
            self.toTemplate.currentPage = UI.getStartPage(self.lang, self.pageRefresh)
            # We need at least one page as startpage
            if self.toTemplate.currentPage is None:
                self.toTemplate.error = { 'code' : '500', 'message' : 'Missing startpage. Select a start page under tab "Page Settings"' }
                return False
            # Get page modules associated with startpage
            pageModule = PageModules.getByPageKeyAndLanguage(self.toTemplate.currentPage.key(), self.lang)
        else:
            # Get page modules associated with url path
            pageModule = PageModules.getByPath(self.path)
        # We need at least one pageModule to display any page
        if pageModule is None:
            self.toTemplate.error = { 'code' : '404', 'message' : 'Can\'t find request page' }
            return False
        else:
            # If no current page is set, set pageModules's page as currentpage
            if not self.toTemplate.currentPage:
                # TODO: Remove reference property since it causes an extra query.
                #self.toTemplate.currentPage = Pages.getByKeyForMainView(pageModule.pageKey.key())
                self.toTemplate.currentPage = pageModule.pageKey
                
            # templateType is stored with entire class path, we only need the last name
            pageTemplateType = self.toTemplate.currentPage.templateType.split('.')[-1]

            # Set up memcacheid based on language
            memcacheid = "mainView_pageTemplate_%s" % self.path
            pageTemplate = memcache.get(memcacheid)
            # If pageTemplate is not in memcache
            if pageTemplate is None or self.pageRefresh:
                # Find pageTemplate class
                pageTemplateClass = getattr(PageTemplates, pageTemplateType, None)
                #invoke class and store it in memcache
                pageTemplate = pageTemplateClass(page = self.toTemplate.currentPage, query = query, language = self.lang)
                pageTemplate.postRender(self.lang, query)
                memcache.set(memcacheid, pageTemplate, Settings.memcacheTimeout)

            # Do stuff after saved to cache
            pageTemplate.postCache(self.lang, query)
            # Bind pageTemplate to view
            self.toTemplate.pageTemplate = pageTemplate
            self.templateFile = pageTemplate.templateFile
            self.toTemplate.pageType = pageTemplateType
            self.toTemplate.pageModule = self.toTemplate.pageTemplate.pageModules[self.lang]
            self.toTemplate.pageContent = self.toTemplate.pageTemplate.pageData[self.lang]
            self.toTemplate.language = self.lang