__author__ = 'broken'

import os
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def PageTree(pages, currentView):
    return  { 'pageTree' : pages, 'currentView': currentView }

path = os.path.join(os.path.dirname(__file__), '../../pac_static/templates/modules/pageTree.html')
register.inclusion_tag(path)(PageTree)

def SitePageTree(pages, currentPage):
    return  { 'pageTree' : pages, 'currentPage': currentPage }

path = os.path.join(os.path.dirname(__file__), '../../templates/modules/sitePageTree.html')
register.inclusion_tag(path)(SitePageTree)

def Module(arg0, arg1, arg2):
    data = ''

    if isinstance(arg0, str) or isinstance(arg0, unicode):
        arg0 = { 'file' : arg0 }
        data = arg1
    else:
        arg0 = arg0
        if arg0['data'].has_key(arg1):
            data = arg0['data'][arg1]

    return  { 'module' : arg0, 'data' : data, 'language' : arg1, 'argument0' : arg2 }

path = os.path.join(os.path.dirname(__file__), '../../pac_static/templates/modules/module.html')
register.inclusion_tag(path)(Module)