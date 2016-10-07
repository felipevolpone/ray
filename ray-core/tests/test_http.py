from ray.http import param_at, get_id, query_params_to_dict
import unittest
from webtest import TestApp
from ray.wsgi.wsgi import application


class TestHttp(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)

    def test_request_param_at(self):
        request = self.app.get('/api/user/123/foo?name=bar')
        self.assertEqual('123', param_at(request.path, 2))
        self.assertEqual('foo', param_at(request.path, 3))
        self.assertEqual('bar', request.params['name'])
        self.assertEqual('foo', param_at(request.path, -1))

        request = self.app.get('/api/user')
        self.assertEqual(None, param_at(request.path, 0))
        self.assertEqual('user', param_at(request.path, 1))
