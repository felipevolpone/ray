from onhands.http import Request
import unittest


class TestHttp(unittest.TestCase):

    def test_request_param_at(self):
        request = Request.blank('/api/user/123/foo?name=bar')
        self.assertEqual('123', request.param_at(0))
        self.assertEqual('foo', request.param_at(1))
        self.assertEqual('bar', request.params['name'])
