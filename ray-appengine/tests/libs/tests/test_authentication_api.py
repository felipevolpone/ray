
import unittest

from webapp2 import Request

from ray.endpoint import RaySettings
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray.authentication import Authentication

from tests.model_interface import ModelInterface


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
        RaySettings.ENDPOINT_MODULES.append('tests.test_authentication_api')

    def test_login(self):
        req = Request.blank('/api/_login', method='POST')
        req.json = {"username": "felipe", "password": '123'}
        response = req.get_response(application)
        cookie = response.headers['Set-Cookie']
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/_login', method='POST')
        req.json = {"username": "felipe", "password": 'admin'}
        response = req.get_response(application)
        self.assertEqual(403, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        response = req.get_response(application)
        self.assertEqual(404, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        req.headers['Cookie'] = cookie
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)
