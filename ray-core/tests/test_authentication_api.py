
import unittest

from webapp2 import Request

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


@unittest.skip('its necessary mock the ModelInterface database')
class TestProctedEndpoint(unittest.TestCase):

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

        req = Request.blank('/api/gamer/', method='GET')
        response = req.get_response(application)
        self.assertEqual(404, response.status_int)

        req = Request.blank('/api/gamer/', method='GET')
        req.headers['Cookie'] = cookie
        response = req.get_response(application)
        self.assertEqual(200, response.status_int)
