
import unittest

from webtest import TestApp as FakeApp

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


@endpoint('/resource', authentication=MyAuth)
class ResourceModel(ModelInterface):

    def __init__(self, *a, **k):
        super(ResourceModel, self).__init__(*a, **k)

    @classmethod
    def columns(cls):
        return ['id']


class TestProctedEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = FakeApp(application)

    def test_login(self):
        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": 'admin'}, expect_errors=True)
        self.assertEqual(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.get('/api/resource/', expect_errors=True)
        self.assertEqual(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/resource/')
        self.assertEqual(200, response.status_int)

    def test_logout(self):
        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/resource/')
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/_logout')
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.get('/api/resource/', expect_errors=True)
        self.assertEqual(401, response.status_int)

