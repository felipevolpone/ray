
import unittest, json

from webapp2 import Request

from ray.wsgi.wsgi import application
from ray.endpoint import endpoint
from ray.authentication import Authentication

from tests.model_interface import ModelInterface


class MyAuth(Authentication):

    salt_key = 'ray_salt_key'

    @classmethod
    def authenticate(cls, login_data):
        if login_data['username'] == 'felipe' and login_data['password'] == '123':
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

    def test_login(self):
        req = Request.blank('/api/_login', method='POST')
        req.json = {'username': 'felipe', 'password': '123'}
        response = req.get_response(application)
        response.charset = 'utf8'
        token = json.loads(response.text)['result']['token']
        self.assertEqual(200, response.status_int)

        req = Request.blank('/api/_login', method='POST')
        req.json = {'username': 'felipe', 'password': 'admin'}
        response = req.get_response(application)
        self.assertEqual(403, response.status_int)

        req = Request.blank('/api/gamer/', method='GET')
        response = req.get_response(application)
        self.assertEqual(404, response.status_int)

        req = Request.blank('/api/gamer/', method='GET', headers={'Authentication': token})
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)