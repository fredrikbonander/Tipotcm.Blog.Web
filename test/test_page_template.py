__author__ = 'broken'

from gaetestbed.datastore import DataStoreTestCase
from google.appengine.ext import db
from Pac.DataFactory import dbPages
from Pac.UI import PageTemplates
import unittest

class TestPages(DataStoreTestCase, unittest.TestCase):
    def setUp(self):
        self.page = dbPages.Pages()
        self.page.name = 'test'
        self.page.put()

    def test_get_standard_page_template(self):
        pageTemplateString = 'StandardPage'
        template = getattr(PageTemplates, pageTemplateString)
        pageTemplate = template(page = self.page)

        self.assertEqual(pageTemplate.templateName, pageTemplateString)

    def test_get_page_template_module_Main_heading(self):
        pageTemplateString = 'StandardPage'
        template = getattr(PageTemplates, pageTemplateString)
        pageTemplate = template(page = self.page)
        pageTemplate.addModules()

        hasMainHeading = False
        for module in pageTemplate.modules:
            if module['name'] == 'MainHeading':
                hasMainHeading = True

        self.assertTrue(hasMainHeading)