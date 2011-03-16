__author__ = 'broken'

from teamcity.unittestpy import TeamcityTestRunner
from Pac import Controller
from Pac import Users
import unittest
import cgi

class TestEditView(unittest.TestCase):
    def test_get_view(self):
        user = Users.getContext()
        user['user']['authenticated'] = True
        user['user']['permissionLevel'] = 1
        currentView = Controller.EditGetHandler(('edit','/Dashboard'), userContext = user, query = cgi.FieldStorage())

        self.assertEqual(currentView.view.templateFile, 'dashboard.html')

    def test_permissionLevel(self):
        user = Users.getContext()
        user['user']['authenticated'] = True
        currentView = Controller.EditGetHandler(('edit','/Dashboard'), userContext = user, query = cgi.FieldStorage())
        
        self.assertEqual(currentView.view.templateFile, 'not_authorized.html')


if __name__ == '__main__':
    unittest.main(testRunner=TeamcityTestRunner())