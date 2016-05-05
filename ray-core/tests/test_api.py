import unittest
from ray.api import ApiHandler
from ray.wsgi.wsgi import application

from webapp2 import Request

from tests.mock import MockResponse


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


class TestWhereAtAPI(unittest.TestCase):

    # FIXME test if the params sent in the url are getting in the sqlalchemy.
    # maybe is a good idea check this inside the ray-sqlalchemy module.
    # this test will just cover the parse of the query parameters to dict
    # and send it to the ModelInterface

    pass
