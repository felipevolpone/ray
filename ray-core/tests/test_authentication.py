
import unittest
from ray.authentication import Authentication
from ray import authentication_helper


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, login_data):
        return login_data;


class MyAuthFail(Authentication):

    @classmethod
    def authenticate(cls, login_data):
        return None


class TestAuthentication(unittest.TestCase):

    def test_login(self):
        user_json = MyAuth.login({'username': 'admin', 'password': 'admin'})
        self.assertEqual(dict, type(user_json))

        with self.assertRaises(Exception):
            Authentication.login({'username': 'admin', 'password': 'admin'})

        with self.assertRaises(Exception):
            MyAuthFail.login({'username': 'admin', 'password': 'admin'})

    def test_cookie_sign(self):
        _, cookie_value = Authentication.sign_cookie({'username': 'felipe', 'password': '123'})
        self.assertTrue(authentication_helper._validate(cookie_value))
        self.assertTrue(Authentication.is_loged(cookie_value))
