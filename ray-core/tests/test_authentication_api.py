
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray.authentication import Authentication, register

from webtest import TestApp as FakeApp
from tests.model_interface import ModelInterface
from .common import Test


@register
class CustomAuthentication(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        if login_data['username'] == 'felipe' and login_data['password'] == '123':
            return {'username': 'felipe', 'profile': 'admin'}


@endpoint('/resource', authentication=CustomAuthentication)
class ResourceModel(ModelInterface):

    def __init__(self, *a, **k):
        super(ResourceModel, self).__init__(*a, **k)

    @classmethod
    def columns(cls):
        return ['id']


class TestProctedEndpoint(Test):

    user_data = {"username": "felipe", "password": '123'}

    def test_login(self):
        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', self.user_data)
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": 'admin'}, expect_errors=True)
        self.assertEqual(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.get('/api/resource/', expect_errors=True)
        self.assertEqual(401, response.status_int)

        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', self.user_data)
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/resource/')
        self.assertEqual(200, response.status_int)

    def test_logged_user(self):
        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', self.user_data)
        self.assertEqual(200, response.status_int)

        response = self.app.post_json('/api/_info')
        self.assertEqual(200, response.status_int)
        self.assertEqual({'result': {'profile': 'admin', 'username': 'felipe'}}, response.json)

    def test_logout(self):
        self.app = FakeApp(application)
        response = self.app.post_json('/api/_login', self.user_data)
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/resource/')
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/_logout')
        self.assertEqual(200, response.status_int)

        self.app = FakeApp(application)
        response = self.app.get('/api/resource/', expect_errors=True)
        self.assertEqual(401, response.status_int)

