
import unittest
from ray.authentication import Authentication


class MyAuth(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        return login_data


class MyAuthFail(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        return None


class MyAuthWithoutSalt(Authentication):

    @classmethod
    def authenticate(cls, login_data):
        return login_data


class TestAuthentication(unittest.TestCase):

    user_data = {'username': 'admin', 'password': 'admin'}

    def test_login_fail(self):
        token = MyAuth.login(self.user_data)
        self.assertIsNotNone(token)

        with self.assertRaises(Exception):
            Authentication.login(self.user_data)

        with self.assertRaises(Exception):
            MyAuthFail.login(self.user_data)

        with self.assertRaises(Exception):
            MyAuthWithoutSalt.login(self.user_data)

        with self.assertRaises(Exception):
            MyAuthWithoutSalt.login(self.user_data)

    def test_parse_infos_sign(self):
        token = MyAuth.login(self.user_data)
        parsed_user_data = MyAuth.unpack_jwt(token)
        print(parsed_user_data)
        self.assertIsNotNone(parsed_user_data)
        self.assertEqual(dict, type(parsed_user_data))
        self.assertEqual(self.user_data, parsed_user_data)

    def test_parse_infos_sign_invalid_generated_token(self):
        MyAuth.login(self.user_data)
        with self.assertRaises(Exception):
            MyAuth.unpack_jwt('my_invalid_token')

    def test_user_loged(self):
        token_obj = MyAuth.login(self.user_data)
        self.assertTrue(MyAuth.is_loged(token_obj))

    def test_user_not_loged(self):
        self.assertFalse(MyAuth.is_loged(''))
        self.assertFalse(MyAuth.is_loged(None))
