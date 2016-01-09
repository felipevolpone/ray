import unittest
from onhands.api.api import app, OnHandsSettings
from onhands.api.endpoint import endpoint
import webapp2
from alabama.models import StringProperty, IntegerProperty, BaseModel
from tests.mock import MockResponse


@endpoint('/user')
class UserModel(BaseModel):
    name = StringProperty()
    age = IntegerProperty()


class TestRouter(unittest.TestCase):

    @unittest.skip('skip')
    def test_basic_router(self):
        request = webapp2.Request.blank('/api/')
        response = request.get_response(app)
        self.assertEqual(200, response.status_int)

    def __create(self):
        request = webapp2.Request.blank('/api/user')
        request.json = {"name": "felipe", "age": 22}
        request.method = 'POST'
        return request.get_response(app)

    @unittest.skip('skip')
    def test_post(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_router'

        # create data
        response = self.__create()
        self.assertEqual(200, response.status_int)

    def test_get(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_router'

        # create data
        response = self.__create()

        request = webapp2.Request.blank('/api/user')
        request.method = 'GET'
        response = MockResponse(request.get_response(app))

        print response.body
        self.assertEqual(response.to_json(), {'result': [{'age': 22, 'name': 'felipe'}]})
        self.assertEqual(200, response.status_int)
