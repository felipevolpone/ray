
import unittest
from onhands.authentication import Authentication
from onhands import authentication_helper


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

    def test_cookie_sign(self):
        _, cookie_value = Authentication.sign_cookie({'username': 'felipe', 'password': '123'})
        self.assertTrue(authentication_helper._validate(cookie_value))
        self.assertTrue(Authentication.is_loged(cookie_value))
#
#
# @protected
# @endpoint('/user')
# class User(Model):
#     name = StringProperty()
#     age = IntegerProperty()
#
#
# class UserActions(Action):
#     __model__ = User
#
#     @action('/vote')
#     def vote(self):
#         pass
