
import unittest

from webtest import TestApp

from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray.authentication import Authentication, register

from tests.model_interface import ModelInterface


@register
class MyAuth(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        if login_data['username'] == 'felipe' and login_data['password'] == '123':
            return {'username': 'felipe'}


@endpoint('/gamer', authentication=MyAuth)
class GamerModel(ModelInterface):

    def __init__(self, *a, **k):
        super(GamerModel, self).__init__(*a, **k)

    @classmethod
    def columns(cls):
        return ['id']


class TestProctedEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)

    def test_login(self):
        self.app = TestApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        self.assertIsNotNone(response.json['result']['token'])
        token = response.json['result']['token']
        self.assertEqual(200, response.status_int)

        self.app = TestApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": 'admin'}, expect_errors=True)
        self.assertEqual(401, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', expect_errors=True)
        self.assertEqual(401, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', headers={'Authentication': str(token)})
        self.assertEqual(200, response.status_int)

    def test_logout(self):
        self.app = TestApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        self.assertIsNotNone(response.json['result']['token'])
        token = response.json['result']['token']
        self.assertEqual(200, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', headers={'Authentication': str(token)})
        self.assertEqual(200, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/_logout', headers={'Authentication': str(token)})
        self.assertEqual(200, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', expect_errors=True)
        self.assertEqual(401, response.status_int)
