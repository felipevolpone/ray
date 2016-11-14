
import unittest
from ray.authentication import Authentication, register
from ray import exceptions


@register
class MyAuth(Authentication):

    salt_key = 'ray_salt_key'
    expiration_time = 5

    @classmethod
    def authenticate(cls, login_data):
        return login_data


@register
class MyAuthFail(Authentication):

    salt_key = 'ray_salt_key'
    expiration_time = 5

    @classmethod
    def authenticate(cls, login_data):
        return None


@register
class MyAuthWithoutSalt(Authentication):

    expiration_time = 5

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
        parsed_user_data = MyAuth.unpack_jwt(token.decode('utf-8'))
        self.assertIsNotNone(parsed_user_data)
        self.assertEqual(dict, type(parsed_user_data))
        self.assertEqual(self.user_data, parsed_user_data)

    def test_parse_infos_sign_invalid_generated_token(self):
        MyAuth.login(self.user_data)
        with self.assertRaises(Exception):
            MyAuth.unpack_jwt('my_invalid_token')

    def test_authentication_expiration_time(self):
        class MyAuthWithoutExpirationTime(Authentication):

            salt_key = 'salt_key'

            @classmethod
            def authenticate(cls, login_data):
                return login_data

        with self.assertRaises(NotImplementedError):
            MyAuthWithoutExpirationTime.login(self.user_data)

    def test_authentication_expiration_time_exception(self):
        class MyAuthExpirationTimeNotAnInteger(Authentication):

            salt_key = 'salt_key'
            expiration_time = 'a'

            @classmethod
            def authenticate(cls, login_data):
                return login_data

        with self.assertRaises(exceptions.AuthenticationExpirationTime):
            MyAuthExpirationTimeNotAnInteger.login(self.user_data)
