from google.appengine.api import memcache
from Pac.DataFactory import dbPages
from Pac.DataFactory import dbPageModules
from Pac.UI import PageTemplates
from Pac import Settings
import inspect

def getPageTemplates():
    module = PageTemplates
    clazz = PageTemplates.BaseTemplate
    return [ cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and issubclass(cls, clazz) and cls is not clazz ]

def getAllPagesForEditView():
    pages = dbPages.Pages.gql('ORDER BY sortIndex').fetch(1000)
    return pages


def getPageTreeForEditView():
    pages = getAllPagesForEditView()
    return buildTree(pages, None, 'parentStringKey', None)


def buildTree(nodes, pageModules, identifier, rootIdentifier):
    # create empty tree to fill
    t = {}
    pageTree = {}
    # Main View is for tree show on main page not edit mode

    # First group all pages w/ same parent
    for node in nodes:
        # Where parentKey is None, this tells us that node is a root level node
        if node.parentStringKey == rootIdentifier:
            key = 'root'
        else:
            key = node.parentStringKey

        if not t.has_key(key):
            t[key] = []

        # If pagemodules are present, we need to store them along side the page object
        # to display proper menu and paths i main view
        if pageModules:
            # TODO: Shouldn't need to loop for every node
            for pageModule in pageModules:
                if pageModule.pageKey.key() == node.key():
                    t[key].append({ 'page' : node, 'pageModule' : pageModule, 'children' : []})
        else:
            t[key].append({ 'page' : node, 'children' : []})

    if t.has_key('root'):
        pageTree = t['root']
    # Iterate over there

    build_page_tree(pageTree, t)

    return pageTree

def build_page_tree(pageTree, nodes):
    #Loop over selected list
    for parent, node in nodes.iteritems():
        # We don't need to loop over the root level node
        if parent is not 'root':
            # Loop over current level in page tree
            for item in pageTree:
                # Match keys
                if str(item['page'].key()) == parent:
                    # Save node as child
                    item['children'] = node
                    # Only need to loop over childs if they are present
                    build_page_tree(item['children'], nodes)


def getStartPage(language, force):
    pageMemcacheId = 'start_page_' + str(language)
    startPage = memcache.get(pageMemcacheId)

    if startPage is None or force:
        startPage = dbPages.Pages.gql('WHERE startPage = True').get()
        if startPage:
            memcache.set(pageMemcacheId, startPage, Settings.memcacheTimeout)

    return startPage

def getAllPagesForMainView():
    pageEntries = dbPages.Pages.gql('ORDER BY sortIndex').fetch(1000)
    return pageEntries

def getPageTreeForMainView(language, memcacheid):
    # Get all pages and order by sort index
    pages = getAllPagesForMainView()
    # Get all published page modules to be match against pages
    pageModules = dbPageModules.PageModules.gql('WHERE lang = :lang AND published = :published', lang = language, published = True).fetch(100)

    pageTree = buildTree(pages, pageModules, 'parentStringKey', None)
    memcache.set(memcacheid, pageTree, Settings.memcacheTimeout)

    return pageTree

def getFooterPageTree(language):
    memcacheId = 'footerPageTree_' + str(language)
    footerPageTree = memcache.get(memcacheId)

    if footerPageTree is None or Settings.forceMemcacheRefresh:
        footerContainer = dbPages.Pages.get_by_key_name('footercontainer')
        if footerContainer:
            footerPages = dbPages.Pages.gql('WHERE parentStringKey = :parentStringKey', parentStringKey = str(footerContainer.key())).fetch(100)
            # Get all published page modules to be match against pages
            pageModules = dbPageModules.PageModules.gql('WHERE lang = :lang AND published = :published', lang = language, published = True).fetch(100)
            footerPageTree = buildTree(footerPages, pageModules, 'parentStringKey', str(footerContainer.key()))
            memcache.set(memcacheId, footerPageTree, Settings.memcacheTimeout)

    return footerPageTree