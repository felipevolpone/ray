import unittest
from ray.api import ApiHandler


class TestApiHandler(unittest.TestCase):

    def test_is_endpoint(self):
        api_handler = ApiHandler()
        self.assertTrue(api_handler.is_endpoint('/api/user'))
        self.assertTrue(api_handler.is_endpoint('/api/user'))
        self.assertTrue(api_handler.is_endpoint('/api/user/123'))
        self.assertFalse(api_handler.is_endpoint('/api/user/123/activate'))

    def test_is_action(self):
        api_handler = ApiHandler()
        self.assertFalse(api_handler.is_action('/api/user'))
        self.assertFalse(api_handler.is_action('/api/user'))
        self.assertFalse(api_handler.is_action('/api/user/123'))
        self.assertTrue(api_handler.is_action('/api/user/123/activate'))
