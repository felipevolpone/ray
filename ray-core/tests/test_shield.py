
import unittest

from webapp2 import Request

from ray.endpoint import endpoint
from ray.wsgi.wsgi import application
from ray.authentication import Authentication
from ray.shield import Shield

from tests.model_interface import ModelInterface


class MyAuth(Authentication):

    @classmethod
    def authenticate(cls, username, password):
        if username == 'felipe' and password == '123':
            return {'username': 'felipe'}


@endpoint('/person')
class PersonModel(ModelInterface):

    def __init__(self, *a, **k):
        self.login = None
        super(PersonModel, self).__init__(*a, **k)

    @classmethod
    def describe(cls):
        return {'login': str}


class PersonShield(Shield):
    __model__ = PersonModel

    def get(self, info):
        return info['username'] == 'felipe'


@unittest.skip('skip')
class TestShield(unittest.TestCase):

    def test(self):
        req = Request.blank('/api/_login', method='POST')
        req.json = {"username": "felipe", "password": '123'}
        response = req.get_response(application)
        cookie = response.headers['Set-Cookie']
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        req.headers['Cookie'] = cookie
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        response = req.get_response(application)
        self.assertEquals(404, response.status_int)

        for http_method in ['POST', 'PUT', 'DELETE']:
            req = Request.blank('/api/person/', method=http_method)
            response = req.get_response(application)
            self.assertIsNot(404, response.status_int)
