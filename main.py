#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.dist import use_library

use_library('django', '1.1')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from Pac import Controller
from Pac import ImageStore
from Pac import Users
from Pac import Setup

import os
import cgi

def render_template(file, template_vals):
    path = os.path.join(os.path.dirname(__file__), file)
    return template.render(path, template_vals)

class EditHandler(webapp.RequestHandler):
    def get(self, *path):
        query = cgi.FieldStorage()
        userContext = Users.getContext()
        currentView = Controller.EditGetHandler(path, query = query, userContext = userContext)

        self.response.out.write(render_template('pac_static/templates/' + currentView.view.templateFile, currentView.view.toTemplate))

    def post(self, *path):
        currentView = Controller.EditPostHandler(path, request = self.request)

        self.redirect(currentView.redirect)

class MainHandler(webapp.RequestHandler):
    def get(self,*path):
        if path[0] == '/':
            self.redirect('/en-us/')
        else:
            query = cgi.FieldStorage()
            userContext = Users.getContext()
            currentView = Controller.MainGetHandler(path, query = query, userContext = userContext)
            self.response.out.write(render_template('templates/' + currentView.view.templateFile, currentView.view.toTemplate))

    def post(self, *path):
        currentView = Controller.MainPostHandler(path, request = self.request)

        self.redirect(currentView.redirect)

def main():
    application = webapp.WSGIApplication([('/edit/setup/', Setup.SetupHandler),
                                          ('/edit/AddUpdateImageStore', ImageStore.AddUpdateImageStore),
                                          (r'/(?i)(Edit)(.*)', EditHandler),
                                          (r'(.*)', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

webapp.template.register_template_library('Pac.TemplateTags')

if __name__ == '__main__':
    main()
