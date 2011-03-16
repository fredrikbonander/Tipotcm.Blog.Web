__author__ = 'broken'
from google.appengine.api import memcache
from google.appengine.ext import db
from Pac.DataFactory import dbPages
from Pac.DataFactory import dbPageModules
from Pac.DataFactory import dbContentModules
from Pac.DataFactory import dbPutQueue
from Pac import Settings
from Pac import Utils


def addNewPage(pageName, pageTemplateType, pageParentKey):
    if pageName == '':
        return { 'status': '-1', 'message': 'No Page name entered' }

    if pageTemplateType == '-1':
        return { 'status': '-1', 'message': 'No Page template selected' }

    if pageParentKey == '-1':
        return { 'status': '-1', 'message': 'No Page parent selected' }

    if pageTemplateType.split('.')[-1] == 'PageContainer':
        keyName = Utils.slugify(unicode(pageName))
        page = dbPages.Pages(key_name=keyName)
        page.sortIndex = 1000
    else:
        page = dbPages.Pages()
        page.sortIndex = 10

    page.name = pageName
    page.templateType = pageTemplateType

    parentStringKey = None
    
    if pageParentKey != '0' and pageTemplateType != 'PageService.PageTemplates.PageContainer':
        parentStringKey = pageParentKey

    page.parentStringKey = parentStringKey

    pageKey = db.put(page)

    return { 'status' : 1, 'message' : 'Page added/updated', 'pageKey' : pageKey, 'redirect' : '/edit/Pages/?item_id=' + str(pageKey.id()) }

def updatePageSettings(pageStringKey, startPage, sortIndex):
    if startPage == "on":
        startPageBool = True
    else:
        startPageBool = False

    if startPageBool:
        pages = dbPages.Pages.all()
        for page in pages:
            page.startPage = False
            page.put()

    currentPage = dbPages.Pages.get(db.Key(pageStringKey))
    currentPage.startPage = startPageBool
    currentPage.sortIndex = int(sortIndex)

    dbPutQueue.append(currentPage)

    if startPageBool:
        return { 'status' : 1, 'message' : 'Updated page settings', 'redirect' : '/edit/Pages/?item_id=' + str(currentPage.key().id()) }
    else:
        return { 'status' : -1, 'message' : 'Remember to set one page as startpage', 'redirect' : '/edit/Pages/?item_id=' + str(currentPage.key().id()) }

def deletePage(pageStringKey):
    currentPage = dbPages.Pages.get(db.Key(pageStringKey))
    childPages = dbPages.Pages.gql('WHERE parentStringKey = :pageStringKey', pageStringKey = pageStringKey).fetch(100)

    if not childPages:
        pageModules = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey', pageKey = currentPage.key()).fetch(100)

        for pageModule in pageModules:
            contentModules = dbContentModules.ContentModules.gql('WHERE pageModuleKey = :pageModuleKey', pageModuleKey = pageModule.key()).fetch(100)
            db.delete(contentModules)

        db.delete(pageModules)
        db.delete(currentPage)
        return { 'status' : 1, 'message' : 'Page deleted', 'pageId' : '0' }
    else:
        return { 'status' : -1, 'message' : 'Page has child pages, delete these first', 'redirect' : '/edit/Pages/?item_id=' + str(currentPage.key().id()) }


def getById(pageId):
    return dbPages.Pages.get_by_id(int(pageId))

def getByKey(pageKey):
    return dbPages.Pages.get(pageKey)

def getByKeyForMainView(pageKey):
    memcacheId = 'page_' + str(pageKey)
    entry = memcache.get(memcacheId)

    if entry is None or Settings.forceMemcacheRefresh:
        entry = getByKey(pageKey)
        memcache.set(memcacheId, entry, Settings.memcacheTimeout)

    return entry

def getPagesByStringKey(stringKey):
    memcacheId = 'pages_by_string_key_' + str(stringKey)
    entry = memcache.get(memcacheId)

    if entry is None or Settings.forceMemcacheRefresh:
        entry = dbPages.Pages.gql('WHERE parentStringKey = :parentStringKey', parentStringKey = stringKey).fetch(100)
        memcache.set(memcacheId, entry, Settings.memcacheTimeout)

    return entry

def getBlogPages():
    return dbPages.Pages.gql('WHERE templateType = :templateType', templateType = 'Pac.UI.PageTemplates.BlogPage').fetch(10)

def getParentPageModuleNameByKeyAndLanguage(pageKey, language):
    page = dbPages.Pages.get(pageKey)
    name = ''
    if page:
        pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey and lang = :language', pageKey = db.Key(page.parentStringKey), language = language).get()
        if pageModule:
            name = pageModule.name
    return name