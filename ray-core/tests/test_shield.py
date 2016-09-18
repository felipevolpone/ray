
import unittest

from webapp2 import Request

from ray.endpoint import endpoint
from ray.wsgi.wsgi import application
from ray.authentication import Authentication
from ray.shield import Shield

from tests.model_interface import ModelInterface


class MyAuth(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        if login_data['username'] == 'felipe' and login_data['password'] == '123':
            return {'username': 'felipe'}


@endpoint('/person', authentication=MyAuth)
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


class TestShield(unittest.TestCase):

    def test(self):
        req = Request.blank('/api/_login', method='POST')
        req.json = {'username': 'felipe', 'password': '123'}
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/person/', method='GET')
        response = req.get_response(application)
        self.assertEquals(404, response.status_int)

        for http_method in ['POST', 'PUT', 'DELETE']:
            req = Request.blank('/api/person/', method=http_method)
            response = req.get_response(application)
            self.assertIsNot(404, response.status_int)
