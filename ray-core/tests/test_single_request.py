
from .common import Test

from ray import application
from ray.single_request import Request, api
from ray.authentication import Authentication, register


@api('/status')
class StatusRequest(Request):

    def get(self, request, response):
        return {'type': 'get'}

    def put(self, request, response):
        return {'type': 'put'}

    def post(self, request, response):
        return {'type': 'post'}

    def delete(self, request, response):
        return {'type': 'delete'}


@api('/ping', authentication=True)
class PingRequest(Request):

    def get(self, request, response):
        return {'status': True}


class TestSingleRequests(Test):

    def test_methods(self):
        fullpath = '/api/status'
        it_has = application.has_single_url(fullpath)
        self.assertTrue(it_has)

    def test_api(self):

        @register
        class DumbAuthentication(Authentication):

            expiration_time = 5

            @classmethod
            def salt_key(cls):
                return 'ray_salt_key'

            @classmethod
            def authenticate(cls, login_data):
                return {'username': 'ray'}

        response = self.app.get('/api/status')
        self.assertEquals(200, response.status_int)
        self.assertEquals({'result': {'type': 'get'}}, response.json)

        response = self.app.post('/api/status')
        self.assertEquals(200, response.status_int)
        self.assertEquals({'result': {'type': 'post'}}, response.json)

        response = self.app.delete('/api/status')
        self.assertEquals(200, response.status_int)
        self.assertEquals({'result': {'type': 'delete'}}, response.json)

        response = self.app.put('/api/status')
        self.assertEquals(200, response.status_int)
        self.assertEquals({'result': {'type': 'put'}}, response.json)

        response = self.app.get('/api/ping', expect_errors=True)
        self.assertEquals(403, response.status_int)

        response = self.app.post_json('/api/_login', {'username': 'any'})
        self.assertEqual(200, response.status_int)

        response = self.app.get('/api/ping')
        self.assertEquals(200, response.status_int)
