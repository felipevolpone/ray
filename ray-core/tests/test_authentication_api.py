
import unittest

from webtest import TestApp

from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray.authentication import Authentication

from tests.model_interface import ModelInterface


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        if username == 'felipe' and password == '123':
            return {'username': 'felipe'}


@endpoint('/gamer', authentication=MyAuth)
class GamerModel(ModelInterface):

    def __init__(self, *a, **k):
        self.login = None
        super(GamerModel, self).__init__(*a, **k)

    @classmethod
    def describe(cls):
        return {'login': str}


class TestProctedEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)

    @unittest.skip('skip')
    def test_login(self):
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        cookie = response.headers['Set-Cookie']
        self.assertEqual(200, response.status_int)

        self.app = TestApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": 'admin'}, expect_errors=True)
        self.assertEqual(403, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', expect_errors=True)
        self.assertEqual(404, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', headers={'Cookie': cookie})
        self.assertEqual(200, response.status_int)

    @unittest.skip('skip')
    def test_logout(self):
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        cookie = response.headers['Set-Cookie']
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/gamer/', headers={'Cookie': cookie})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/_logout', headers={'Cookie': cookie})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/gamer/', expect_errors=True)
        self.assertEqual(404, response.status_int)
