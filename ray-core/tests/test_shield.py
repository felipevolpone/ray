
import unittest
from webtest import TestApp

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

    def setUp(self):
        self.app = TestApp(application)

    @unittest.skip('skip')
    def test(self):
        response = self.app.post_json('/api/_login', {"username": "felipe", "password": '123'})
        cookie = response.headers['Set-Cookie']
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/person/', headers={'RayAuth': cookie})
        self.assertEqual(200, response.status_int)

        self.app = TestApp(application)
        response = self.app.get('/api/person', expect_errors=True)
        self.assertEquals(404, response.status_int)

        response = self.app.post('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)

        response = self.app.put('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)

        response = self.app.delete('/api/person/', expect_errors=True)
        self.assertIsNot(404, response.status_int)
