
from .common import Test
from ray import application
from ray.single_request import Request, api


@api('/status')
class StatusRequest(Request):

    def get(self, request, response):
        return {'status': True}


class TestSingleRequests(Test):

    def test(self):
        fullpath = '/api/status'
        it_has = application.has_single_url(fullpath)
        self.assertTrue(it_has)

        response = self.app.get('/api/status')
        self.assertEquals(200, response.status_int)
        self.assertEquals({'result': {'status': True}}, response.json)
