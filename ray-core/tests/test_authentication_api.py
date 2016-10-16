
import unittest

from webtest import TestApp

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

    def setUp(self):
        self.app = TestApp(application)

    @unittest.skip('skip')
    def test_login(self):

# <<<<<<< HEAD
#         response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
#         cookie = response.headers['Set-Cookie']
#         self.assertEqual(200, response.status_int)

#         self.app = TestApp(application)
#         response = self.app.post_json('/api/_login', {"username": "felipe", "password": 'admin'}, expect_errors=True)
# =======

        # req = Request.blank('/api/_login', method='POST')
        # req.json = {'username': 'felipe', 'password': '123'}
        # response = req.get_response(application)
        # response.charset = 'utf8'
        # token = json.loads(response.text)['result']['token']
        # self.assertEqual(200, response.status_int)

        # req = Request.blank('/api/_login', method='POST')
        # req.json = {'username': 'felipe', 'password': 'admin'}
        # response = req.get_response(application)
        # self.assertEqual(403, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', expect_errors=True)
        self.assertEqual(404, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/gamer/', headers={'Cookie': cookie})
        self.assertEqual(200, response.status_int)

        # req = Request.blank('/api/gamer/', method='GET', headers={'Authentication': token})
        # response = req.get_response(application)
        # self.assertEqual(200, response.status_int)

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
