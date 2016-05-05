
import unittest, requests
from .app import User
import json


def build_url(id_=None, params=None):
    base = 'http://localhost:8080/api/user'
    if params:
        base = base + params
    return base + '/' + id_ if id_ else base


@unittest.skip('skp')
class TestIntegrated(unittest.TestCase):

    def test_columns(self):
        columns = User.columns()
        self.assertEqual(['age', 'id', 'name'], columns)

    def _create(self, name=None, age=None):
        data = json.dumps({'age': age, 'name': name})
        return requests.post(build_url(), data=data)

    def test_api(self):
        # test post create
        resp = self._create(name='felipe', age=22)
        result = json.loads(resp.content)['result']
        self.assertEqual(result['name'], 'felipe')
        self.assertEqual(result['age'], 22)
        self.assertIsNotNone(result['id'])
        id_created = str(result['id'])

        self._create(name='john', age=26)

        # test get all
        resp = requests.get(build_url())
        result = json.loads(resp.content)['result']
        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 22)
        self.assertIsNotNone(result[0]['id'])
        self.assertEqual(result[1]['name'], 'john')

        # test get by id
        resp = requests.get(build_url(id_created))
        result = json.loads(resp.content)['result']
        self.assertEqual('felipe', result['name'])
        self.assertEqual(22, result['age'])

        # test update
        data = json.dumps({'name': 'felipe volpone'})
        resp = requests.put(build_url(id_created), data=data)
        self.assertEqual(200, resp.status_code)

        resp = requests.get(build_url(id_created))
        result = json.loads(resp.content)['result']
        self.assertEqual('felipe volpone', result['name'])
        self.assertEqual(22, result['age'])
        self.assertEqual(int(id_created), result['id'])

        # test delete
        resp = requests.delete(build_url(id_created))
        self.assertEqual(200, resp.status_code)

        # test get
        resp = requests.get(build_url(id_created))
        self.assertEqual(404, resp.status_code)


class TestWhereAtAPI(unittest.TestCase):

    # FIXME test if the params sent in the url are getting in the sqlalchemy.
    # maybe is a good idea check this inside the ray-sqlalchemy module.
    # this test will just cover the parse of the query parameters to dict
    # and send it to the ModelInterface

    def _create(self, name=None, age=None):
        data = json.dumps({'age': age, 'name': name})
        return requests.post(build_url(), data=data)

    def test_query_params(self):
        for name in 'felipe joao roberto'.split():
            self._create(name=name)

        resp = requests.get(build_url(params="?name=felipe"))
        self.assertEqual(200, resp.status_code)
        result = json.loads(resp.content)['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'felipe')
