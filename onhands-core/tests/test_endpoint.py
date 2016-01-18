from onhands.api import OnHandsSettings
from onhands.wsgi.wsgi import application
from onhands.http import Request
from onhands.endpoint import endpoint

from alabama.models import StringProperty, IntegerProperty, BaseModel
from tests.mock import MockResponse, TestMock

import alabamaonhands.all as alabama_it
from tests import storage as storage_test
alabama_it.storage = storage_test

import unittest


@endpoint('/user')
class UserModel(alabama_it.AlabamaModel):
    name = StringProperty()
    age = IntegerProperty()


class TestEndpoint(TestMock):

    def setUp(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_endpoint'
    
    @unittest.skip('skip')
    def test_404(self):
        request = Request.blank('/api/', method='GET')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)

    def __create(self):
        request = Request.blank('/api/user', method='POST')
        request.json = {"name": "felipe", "age": 22}
        return MockResponse(request.get_response(application))

    def test_post(self):
        response = self.__create()
        self.assertEqual(200, response.status_int)

    @unittest.skip('skip')
    def test_get_all(self):
        self.__create()
        self.__create()

        request = Request.blank('/api/user', method='GET')
        response = MockResponse(request.get_response(application))

        result = response.to_json()
        self.assertEqual(2, len(result['result']))
        self.assertEqual('felipe', result['result'][0]['name'])
        self.assertEqual(22, result['result'][0]['age'])
        self.assertEqual(200, response.status_int)
    
    def test_get(self):
        self.__create()
        rsp = self.__create()
        result_create = rsp.to_json()
        uuid_created = result_create['result']['uuid']

        request = Request.blank('/api/user/' + uuid_created, method='GET')
        response = MockResponse(request.get_response(application))

        result = response.to_json()
        self.assertEqual(result['result']['uuid'], uuid_created)
        self.assertEqual(200, response.status_int)

        request = Request.blank('/api/user/wrong_uuid', method='GET')
        response = request.get_response(application)
        self.assertEqual(500, response.status_int)
    
    def test_put(self): 
        self.__create()
        rsp = self.__create()
        result_create = rsp.to_json()
        uuid_created = result_create['result']['uuid']

        request = Request.blank('/api/user/' + uuid_created, method='PUT')
        request.json = {"name": "onhands", 'uuid': uuid_created}
        response = MockResponse(request.get_response(application))

        result = response.to_json()
        self.assertEqual(result['result']['uuid'], uuid_created)
        self.assertEqual(result['result']['name'], 'onhands')
        self.assertEqual(result['result']['age'], 22)
        self.assertEqual(200, response.status_int)

    @unittest.skip('slip')
    def test_delete(self):
        self.__create()
        rsp = self.__create()
        result_create = MockResponse(rsp).to_json()
        id_created = result_create['result']['uuid']

        request = Request.blank('/api/user/' + id_created, method='DELETE')
        response = MockResponse(request.get_response(application))

        result = response.to_json()
        self.assertEqual(result['result']['uuid'], id_created)
        self.assertEqual(200, response.status_int)

