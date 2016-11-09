import unittest
from ray.api import _is_endpoint, _is_action


class TestApiHandler(unittest.TestCase):

    def test_is_endpoint(self):
        self.assertTrue(_is_endpoint('/api/user'))
        self.assertTrue(_is_endpoint('/api/user'))
        self.assertTrue(_is_endpoint('/api/user/123'))
        self.assertFalse(_is_endpoint('/api/user/123/activate'))

    def test_is_action(self):
        self.assertFalse(_is_action('/api/user'))
        self.assertFalse(_is_action('/api/user'))
        self.assertFalse(_is_action('/api/user/123'))
        self.assertTrue(_is_action('/api/user/123/activate'))
