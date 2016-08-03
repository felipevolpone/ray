from ray.http import param_at, get_id, query_params_to_dict
from webapp2 import Request
import unittest


class TestHttp(unittest.TestCase):

    def test_request_param_at(self):
        request = Request.blank('/api/user/123/foo?name=bar')
        self.assertEqual('123', param_at(request.path, 2))
        self.assertEqual('foo', param_at(request.path, 3))
        self.assertEqual('bar', request.params['name'])
        self.assertEqual('foo', param_at(request.path, -1))

        request = Request.blank('/api/user')
        self.assertEqual(None, param_at(request.path, 0))
        self.assertEqual('user', param_at(request.path, 1))

    def test_parse_params(self):
        request = Request.blank('/api/user?name=felipe&age=23', method='GET')
        self.assertEqual({'name': 'felipe', 'age': 23}, query_params_to_dict(request))
