import unittest
import webtest

from webtest import TestApp
#from ray.wsgi.wsgi import application
from ray.api import application
from ray.endpoint import endpoint

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
        self.app = TestApp(application)

    def test_404(self):
        response = self.app.get('/api/', expect_errors=True)
        self.assertEqual(404, response.status_int)

    def __create(self):
        return self.app.post_json('/api/user', {"name": "felipe", "age": 22})

    def test_post(self):
        resp = self.__create()
        result = resp.json
        print result
        self.assertEqual('felipe', result['result']['name'])
        self.assertEqual(200, resp.status_int)

    @unittest.skip('skip')
    def test_get_all(self):
        self.__create()

        request = Request.blank('/api/user', method='GET')
        response = MockResponse(request.get_response(application))
        self.assertEqual(200, response.status_int)

    @unittest.skip('skip')
    def test_get(self):
        uuid_created = '1245'
        request = Request.blank('/api/user/' + uuid_created, method='GET')
        response = MockResponse(request.get_response(application))
        self.assertEqual(200, response.status_int)

    @unittest.skip('skip')
    def test_put(self):
        uuid_created = '1245'
        request = Request.blank('/api/user/' + uuid_created, method='PUT')
        request.json = {"name": "ray", 'uuid': uuid_created}
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

    @unittest.skip('skip')
    def test_delete(self):
        uuid_created = '1245'
        request = Request.blank('/api/user/' + uuid_created, method='DELETE')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)
