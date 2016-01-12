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

        result = response.to_json()
        self.assertEqual(2, len(result['result']))
        self.assertEqual('felipe', result['result'][0]['name'])
        self.assertEqual(22, result['result'][0]['age'])
        self.assertEqual(200, response.status_int)

    def test_get(self):
        # create data
        self.__create()
        rsp = self.__create()
        result_create = MockResponse(rsp).to_json()
        uuid_created = result_create['result']['uuid']

        request = Request.blank('/api/user/'+uuid_created)
        request.method = 'GET'
        response = MockResponse(request.get_response(app))

        result = response.to_json()
        self.assertEqual(result['result']['uuid'], uuid_created)
        self.assertEqual(200, response.status_int)
