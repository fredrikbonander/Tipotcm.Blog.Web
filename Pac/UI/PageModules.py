__author__ = 'broken'
from google.appengine.api import memcache
from google.appengine.ext import db
from Pac.DataFactory import dbPageModules
from Pac.DataFactory import dbPages
from Pac import Utils
from Pac import Settings

def addUpdatePageModule(pageStringKey, pageModuleName, language, publish):
    pageKey = db.Key(pageStringKey)

    if publish == "on":
        publish = True
    else:
        publish = False

    page = dbPages.Pages.get(pageKey)
    pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :language', pageKey = pageKey, language = language).get()

    if pageModule is None:
        pageModule = dbPageModules.PageModules()
        pageModule.pageKey = pageKey
        pageModule.lang = language

    pageModule.name = pageModuleName
    stringPath = Utils.slugify(unicode(pageModuleName)) + '/'
    path = getPath(page, language, stringPath)

    ## If path is False, parent page in GetPath method has not been saved.
    if not path:
        return { 'status' : -1, 'message' : 'Parent page is not published', 'pageId' : str(page.key().id()) }

    pageModule.path = path
    pageModule.published = publish

    ## We need the key so we put this in the datastore right away
    pageModuleKey = db.put(pageModule)

    return { 'status' : 1, 'message' : 'Content added/updated', 'redirect' : '/edit/Pages/?item_id=' + str(page.key().id()), 'pageModuleKey' : pageModuleKey }

def getPath(page, language, path):
    if page.parentStringKey is None:
        return '/' + language + '/' + path
    else:
        page = dbPages.Pages.get(db.Key(page.parentStringKey))
        if page.templateType.split('.')[-1] == 'PageContainer':
            return '/' + language + '/' + path

        pageModule = dbPageModules.PageModules.gql('WHERE published = True AND pageKey = :pageKey AND lang = :language', pageKey = page.key(), language = language).get()

        if pageModule is None:
            return False

        return pageModule.path + path

def getByPageKey(pageKey):
    return dbPageModules.PageModules.gql('WHERE pageKey = :pageKey', pageKey = pageKey).fetch(1000)

def getByPageKeyAndLanguage(pageKey, language):
    memcacheId = 'pageModule_' + str(pageKey) + '_' + str(language)
    pageModule = memcache.get(memcacheId)

    if pageModule is None or Settings.forceMemcacheRefresh:
        pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang', pageKey = pageKey, lang = language).get()
        memcache.set(memcacheId, pageModule, Settings.memcacheTimeout)
        
    return pageModule

def getByPath(path):
    memcacheId = 'pageModule_' + str(path)
    pageModule = memcache.get(memcacheId)

    if pageModule is None or Settings.forceMemcacheRefresh:
        pageModule = dbPageModules.PageModules.gql('WHERE path = :path', path = path).get()
        memcache.set(memcacheId, pageModule, Settings.memcacheTimeout)

    return pageModule