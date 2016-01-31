from onhands.http import param_at
from webapp2 import Request
import unittest


class TestHttp(unittest.TestCase):

    def test_request_param_at(self):
        request = Request.blank('/api/user/123/foo?name=bar')
        self.assertEqual('123', param_at(request.upath_info, 0))
        self.assertEqual('foo', param_at(request.upath_info, 1))
        self.assertEqual('bar', request.params['name'])

        request = Request.blank('api/user')
        self.assertEqual(None, param_at(request.upath_info, 0))
