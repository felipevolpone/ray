import unittest
from ray.api import is_endpoint, is_action


class TestApiHandler(unittest.TestCase):

    def test_is_endpoint(self):
        self.assertTrue(is_endpoint('/api/user'))
        self.assertTrue(is_endpoint('/api/user'))
        self.assertTrue(is_endpoint('/api/user/123'))
        self.assertFalse(is_endpoint('/api/user/123/activate'))

    def test_is_action(self):
        self.assertFalse(is_action('/api/user'))
        self.assertFalse(is_action('/api/user'))
        self.assertFalse(is_action('/api/user/123'))
        self.assertTrue(is_action('/api/user/123/activate'))
