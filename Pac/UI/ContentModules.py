__author__ = 'broken'

from google.appengine.api import memcache
from google.appengine.ext import db
from Pac.DataFactory import dbContentModules
from Pac.DataFactory import dbPutQueue
from Pac import Settings

def addUpdateContentModule(pageModuleKey, params):
    args = params.arguments()
    for arg in args:
        argList = arg.split('|')
        if len(argList) > 1:
            contentModuleName = argList[0]
            contentModuleType = argList[1]

            if contentModuleType == 'static' or contentModuleType == 'singleImage' or contentModuleType == 'multipleImages':
                addUpdateStaticContentModule(pageModuleKey, contentModuleName, params.get(arg))

    #return { 'status' : 1, 'message' : 'Content added/updated', 'pageId' : str(page.key().id()) }

def addNewContentModule(pageModuleKey, contentModuleName):
    contentModule = dbContentModules.ContentModules()
    contentModule.pageModuleKey = pageModuleKey
    contentModule.name = contentModuleName

    return contentModule

def addUpdateStaticContentModule(pageModuleKey, contentModuleName, content):
    contentModule = dbContentModules.ContentModules.gql('WHERE pageModuleKey = :pageModuleKey AND name = :name', pageModuleKey = pageModuleKey, name = contentModuleName).get()

    if contentModule is None:
        contentModule = addNewContentModule(pageModuleKey,contentModuleName)

    contentModule.content = content
    db.put(contentModule)
    #dbPutQueue.append(contentModule)

    return contentModule

def getByPageModuleKey(pageModuleKey):
    return dbContentModules.ContentModules.gql('WHERE pageModuleKey = :pageModuleKey', pageModuleKey = pageModuleKey).fetch(100)


def getByNameAndPageModuleKey(name, pageModuleKey):
    memcacheId = 'contentModule_' + str(name) + '_' + str(pageModuleKey)
    entry = memcache.get(memcacheId)

    if entry is None or Settings.forceMemcacheRefresh:
        entry = dbContentModules.ContentModules.gql('WHERE name = :name AND pageModuleKey = :pageModuleKey', name = name, pageModuleKey = pageModuleKey).get()
        memcache.set(memcacheId, entry, Settings.memcacheTimeout)

    return entry