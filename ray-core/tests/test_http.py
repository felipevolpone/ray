from ray.http import param_at, get_id, query_params_to_dict
from webapp2 import Request
import unittest


class TestHttp(unittest.TestCase):

    def test_request_param_at(self):
        request = Request.blank('/api/user/123/foo?name=bar')
        self.assertEqual('123', param_at(request.upath_info, 3))
        self.assertEqual('foo', param_at(request.upath_info, 4))
        self.assertEqual('bar', request.params['name'])
        self.assertEqual('foo', param_at(request.upath_info, -1))

        request = Request.blank('api/user')
        self.assertEqual(None, param_at(request.upath_info, 0))
        self.assertEqual('api', param_at(request.upath_info, 1))

        request = Request.blank('/api/user/fc19dfc03e8344db8058ebc44a2065c6')
        self.assertEqual('fc19dfc03e8344db8058ebc44a2065c6', param_at(request.upath_info, 3))

        self.assertEqual('fc19dfc03e8344db8058ebc44a2065c6', get_id(request.upath_info))

    def test_parse_params(self):
        request = Request.blank('/api/user?name=felipe&age=23', method='GET')
        self.assertEqual({'name': 'felipe', 'age': 23}, query_params_to_dict(request))
