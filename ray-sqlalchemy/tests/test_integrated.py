
import unittest
import json
from .app import User
from webapp2 import Request
from ray.http import Response
from .app import application


class MockResponse(Response):

    def __init__(self, instance):
        Response.__init__(self, instance.json)

    def to_json(self):
        result = {}
        if not self._json:
            return {}

        for key, value in self._json.items():
            key = key.encode('utf-8')
            if type(value) is unicode:
                value = value.encode('utf-8')

            result[key] = value
        return result


def build_url(id_=None, params=None):
    base = 'http://localhost:8080/api/user'
    if params:
        base = base + params
    return base + '/' + id_ if id_ else base


class TestIntegrated(unittest.TestCase):

    def test_columns(self):
        self.assertEqual(['age', 'id', 'name'], User.columns())

    def _create(self, name=None, age=None):
        request = Request.blank(build_url(), method='POST')
        request.json = {'age': age, 'name': name}
        return MockResponse(request.get_response(application))

    def test_api(self):
        # test post create
        resp = self._create(name='felipe', age=22)
        result = resp.to_json()['result']
        self.assertEqual(result['name'], 'felipe')
        self.assertEqual(result['age'], 22)
        self.assertIsNotNone(result['id'])
        id_created = str(result['id'])

        self._create(name='john', age=26)

        # test get all
        req = Request.blank(build_url(), method='GET')
        resp = MockResponse(req.get_response(application))
        result = resp.to_json()['result']
        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 22)
        self.assertIsNotNone(result[0]['id'])
        self.assertEqual(result[1]['name'], 'john')

        # test get by id
        req = Request.blank(build_url(id_created), method='GET')
        resp = MockResponse(req.get_response(application))
        result = resp.to_json()['result']
        self.assertEqual('felipe', result['name'])
        self.assertEqual(22, result['age'])

        # test update
        req = Request.blank(build_url(id_created), method='PUT')
        req.json = {'name': 'felipe volpone'}
        resp = MockResponse(req.get_response(application))
        self.assertEqual(200, resp.status_code)

        req = Request.blank(build_url(id_created), method='GET')
        resp = MockResponse(req.get_response(application))
        result = resp.to_json()['result']
        self.assertEqual('felipe volpone', result['name'])
        self.assertEqual(22, result['age'])
        self.assertEqual(int(id_created), result['id'])

        # test delete
        req = Request.blank(build_url(id_created), method='DELETE')
        resp = req.get_response(application)
        self.assertEqual(200, resp.status_code)

        # test get
        req = Request.blank(build_url(id_created), method='GET')
        resp = req.get_response(application)
        self.assertEqual(404, resp.status_code)


@unittest.skip('skip')
class TestWhereAtAPI(unittest.TestCase):

    def _create(self, name=None, age=None):
        data = {'age': age, 'name': name}
        return requests.post(build_url(), data=data)

    def test_query_params(self):
        for name, age in [('felipe', 35), ('joao', 23), ('roberto', 55), ('roberto', 53)]:
            self._create(name=name, age=age)

        resp = requests.get(build_url(params="?name=felipe"))
        self.assertEqual(200, resp.status_code)
        result = resp.to_json()['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 35)

        resp = requests.get(build_url(params="?age=23"))
        self.assertEqual(200, resp.status_code)
        result = json.loads(resp.content)['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'joao')

        resp = requests.get(build_url(params="?name=roberto"))
        self.assertEqual(200, resp.status_code)
        result = json.loads(resp.content)['result']
        self.assertEqual(2, len(result))
        self.assertEqual(result[0]['age'], 55)
        self.assertEqual(result[1]['age'], 53)

        resp = requests.get(build_url(params="?name=roberto&age=53"))
        self.assertEqual(200, resp.status_code)
        result = json.loads(resp.content)['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'roberto')
        self.assertEqual(result[0]['age'], 53)
