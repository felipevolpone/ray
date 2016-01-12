import unittest
from onhands.api import app, OnHandsSettings
from onhands.http import Request
from onhands.endpoint import endpoint
from alabama.models import StringProperty, IntegerProperty, BaseModel
from tests.mock import MockResponse, TestMock


@endpoint('/user')
class UserModel(BaseModel):
    name = StringProperty()
    age = IntegerProperty()


class TestEndpoint(TestMock):

    def setUp(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_endpoint'

    def test_404(self):
        request = Request.blank('/api/')
        request.method = 'GET'
        response = request.get_response(app)
        self.assertEqual(404, response.status_int)

    def __create(self):
        request = Request.blank('/api/user')
        request.json = {"name": "felipe", "age": 22}
        request.method = 'POST'
        return request.get_response(app)

    def test_post(self):
        # create data
        response = self.__create()
        self.assertEqual(200, response.status_int)

    def test_get_without_params(self):
        # create data
        self.__create()
        self.__create()

        request = Request.blank('/api/user')
        request.method = 'GET'
        response = MockResponse(request.get_response(app))

        self.assertEqual(response.to_json(),
                         {'result': [{'age': 22, 'name': 'felipe'},
                                     {'age': 22, 'name': 'felipe'}]})
        self.assertEqual(200, response.status_int)

    @unittest.skip('skip')
    def test_get(self):
        # create data
        self.__create()
        self.__create()

        request = Request.blank('/api/user/foo')
        request.method = 'GET'
        response = MockResponse(request.get_response(app))

        self.assertEqual(response.to_json(),
                         {'result': [{'age': 22, 'name': 'felipe'},
                                     {'age': 22, 'name': 'felipe'}]})
        self.assertEqual(200, response.status_int)
