__author__ = 'broken'

from teamcity.unittestpy import TeamcityTestRunner
from gaetestbed import DataStoreTestCase

from Pac.DataFactory import dbPages
from Pac.UI import PageModules
from Pac.UI import ContentModules
from Pac.UI import Pages
from Pac import UI

import unittest

class TestPages(DataStoreTestCase, unittest.TestCase):
    def setUp(self):
        self.page = dbPages.Pages()
        self.page.name = 'test'
        self.page.put()

        stringKey = str(self.page.key())
        message = PageModules.addUpdatePageModule(stringKey, 'test', 'se-sv', 'on')
        self.pageModuleKey = message['pageModuleKey']

    def test_add_new_page(self):
        pageName = 'Dummy'
        pageTemplate = 'PageService.PageTemplates.StandardPage'
        pageParentKey = '0'

        message = Pages.addNewPage(pageName, pageTemplate, pageParentKey)

        page = Pages.getByKey(message['pageKey'])

        self.assertEqual(page.name, pageName)

    def test_add_new_page_no_page_name(self):
        message = Pages.addNewPage('', '1', '1')

        self.assertEquals(message['status'], '-1')
    def test_add_new_page_no_page_template(self):
        message = Pages.addNewPage('dummy', '-1', '1')

        self.assertEquals(message['status'], '-1')

    def test_add_new_page_no_page_parent(self):
        message = Pages.addNewPage('dummy', '1', '-1')

        self.assertEquals(message['status'], '-1')

    def test_add_new_page_container(self):
        pageName = 'Dummy'
        pageTemplate = 'PageService.PageTemplates.PageContainer'
        pageParentKey = '0'

        message = Pages.addNewPage(pageName, pageTemplate, pageParentKey)

        page = Pages.getByKey(message['pageKey'])

        self.assertEqual(page.name, pageName)

    def test_get_page_templates_list(self):
        templatesList = UI.getPageTemplates()

        self.assertTrue(len(templatesList) > 0)

    def test_add_new_page_module(self):

        self.assertTrue(self.pageModuleKey)

    def test_add_new_content_module(self):
        contentModule = ContentModules.addUpdateStaticContentModule(self.pageModuleKey, 'test', 'contentTest')

        self.assertEquals(contentModule.content, 'contentTest')

if __name__ == '__main__':
    unittest.main(testRunner=TeamcityTestRunner())