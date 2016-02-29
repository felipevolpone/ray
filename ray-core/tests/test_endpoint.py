import unittest

from webapp2 import Request

from ray.endpoint import RaySettings
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray.authentication import Authentication

from tests.mock import MockResponse
from tests.model_interface import ModelInterface


@endpoint('/user')
class UserModel(ModelInterface):

    def __init__(self, *a, **k):
        self.name = None
        self.age = None
        super(UserModel, self).__init__(*a, **k)

    @classmethod
    def describe(cls):
        return {'name': str, 'age': int}


class TestEndpoint(unittest.TestCase):

    def setUp(self):
        RaySettings.ENDPOINT_MODULES.append('tests.test_endpoint')

    def test_404(self):
        request = Request.blank('/api/', method='GET')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)

    def __create(self):
        request = Request.blank('/api/user', method='POST')
        request.json = {"name": "felipe", "age": 22}
        return MockResponse(request.get_response(application))

    def test_post(self):
        resp = self.__create()
        result = resp.to_json()
        self.assertEqual('felipe', result['result']['name'])
        self.assertEqual(200, resp.status_int)

    def test_get_all(self):
        self.__create()

        request = Request.blank('/api/user', method='GET')
        response = MockResponse(request.get_response(application))
        self.assertEqual(200, response.status_int)

    def test_get(self):
        uuid_created = 'h12u3189adjs'
        request = Request.blank('/api/user/' + uuid_created, method='GET')
        response = MockResponse(request.get_response(application))
        self.assertEqual(200, response.status_int)

    def test_put(self):
        uuid_created = 'h12u3189adjs'
        request = Request.blank('/api/user/' + uuid_created, method='PUT')
        request.json = {"name": "ray", 'uuid': uuid_created}
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

    def test_delete(self):
        uuid_created = 'h12u3189adjs'
        request = Request.blank('/api/user/' + uuid_created, method='DELETE')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        if username == 'felipe' and password == '123':
            return {'username': 'felipe'}


@endpoint('/person', authentication=MyAuth)
class PersonModel(ModelInterface):

    def __init__(self, *a, **k):
        self.login = None
        super(PersonModel, self).__init__(*a, **k)

    @classmethod
    def describe(cls):
        return {'login': str}


class TestProctedEndpoint(unittest.TestCase):

    def setUp(self):
        RaySettings.ENDPOINT_MODULES.append('tests.test_endpoint')

    def test_login(self):
        req = Request.blank('/api/person/login', method='POST')
        req.json = {"username": "felipe", "password": '123'}
        response = req.get_response(application)
        cookie = response.headers['Set-Cookie']
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/person/login', method='POST')
        req.json = {"username": "felipe", "password": 'admin'}
        response = req.get_response(application)
        self.assertEqual(403, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        response = req.get_response(application)
        self.assertEqual(403, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        req.headers['Cookie'] = cookie
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)
