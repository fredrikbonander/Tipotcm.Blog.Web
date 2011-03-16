__author__ = 'broken'
from teamcity.unittestpy import TeamcityTestRunner
import unittest
from gaetestbed import DataStoreTestCase
from Pac.DataFactory.dbUser import User
from Pac import Setup

class TestSetup(DataStoreTestCase, unittest.TestCase):
    def test_add_user(self):
        self.assertEqual(User.all().count(), 0)

        Setup.addFirstTimeUser()

        self.assertEqual(User.all().count(), 1)
        ## Rerun
        Setup.addFirstTimeUser()
        self.assertEqual(User.all().count(), 1)

    def test_get_all_users(self):
        self.assertTrue(User.all() > 0)

if __name__ == '__main__':
    unittest.main(testRunner=TeamcityTestRunner())