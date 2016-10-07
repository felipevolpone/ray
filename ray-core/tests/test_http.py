from ray.http import param_at, get_id, query_params_to_dict
import unittest
from webtest import TestApp
from ray.wsgi.wsgi import application


class TestHttp(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)

    def test_request_param_at(self):
        url = '/api/user/123/foo?name=bar'
        self.assertEqual('123', param_at(url, 2))

        url = '/api/user'
        self.assertEqual(None, param_at(url, 0))
        self.assertEqual('user', param_at(url, 1))
