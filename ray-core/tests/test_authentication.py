
import unittest, jwt
from ray.authentication import Authentication
from ray import authentication_helper


class MyAuth(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        return login_data;


class MyAuthFail(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        return None

class MyAuthWithoutSalt(Authentication):

    @classmethod
    def authenticate(cls, login_data):
        return login_data

user_data = {'username': 'admin', 'password': 'admin'};

class TestAuthentication(unittest.TestCase):

    def test_login(self):
        user_json = MyAuth.login(user_data)
        self.assertEqual(dict, type(user_json))
        self.assertTrue(user_json['token'])

        with self.assertRaises(Exception):
            Authentication.login(user_data)

        with self.assertRaises(Exception):
            MyAuthFail.login(user_data)

        with self.assertRaises(Exception):
            MyAuthWithoutSalt.login(user_data)

    def test_jwt_infos_sign(self):
        token_obj = MyAuth.login(user_data)
        parsed_user_data = jwt.decode(token_obj['token'], 'ray_salt_key', algorithms=['HS256'])
        self.assertEqual(dict, type(parsed_user_data))
        self.assertEqual(user_data, parsed_user_data)

    def test_jwt_infos_sign_wrong_salt_key(self):
        token_obj = MyAuth.login(user_data)
        with self.assertRaises(Exception):
            jwt.decode(token_obj['token'], 'wrong_salt_key', algorithms=['HS256'])
