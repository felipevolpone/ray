
import unittest
from onhands.authentication import Authentication


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        return {'username': username, 'password': password}


class MyAuthFail(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        return None


class TestAuthentication(unittest.TestCase):

    def test_login(self):
        user_json = MyAuth.login('admin', 'admin')
        self.assertEqual(dict, type(user_json))

        with self.assertRaises(Exception):
            Authentication.login('admin', 'admin')

        with self.assertRaises(Exception):
            MyAuthFail.login('admin', 'admin')
