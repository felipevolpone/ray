import unittest, webapp2
from onhands.api import app, OnHandsSettings
from onhands.endpoint import endpoint
from alabama.models import StringProperty, IntegerProperty, BaseModel
from tests.mock import MockResponse


@endpoint('/user')
class UserModel(BaseModel):
    name = StringProperty()
    age = IntegerProperty()


class TestRouter(unittest.TestCase):

    def setUp(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_router'

    def test_404(self):
        request = webapp2.Request.blank('/api/')
        request.method = 'GET'
        response = request.get_response(app)
        self.assertEqual(404, response.status_int)

    def __create(self):
        request = webapp2.Request.blank('/api/user')
        request.json = {"name": "felipe", "age": 22}
        request.method = 'POST'
        return request.get_response(app)

    def test_post(self):
        # create data
        response = self.__create()
        self.assertEqual(200, response.status_int)

    def test_get(self):
        # create data
        response = self.__create()
        response = self.__create()

        request = webapp2.Request.blank('/api/user')
        request.method = 'GET'
        response = MockResponse(request.get_response(app))

        print response.body
        self.assertEqual(response.to_json(),
                         {'result': [{'age': 22, 'name': 'felipe'},
                                     {'age': 22, 'name': 'felipe'}]})
        self.assertEqual(200, response.status_int)
