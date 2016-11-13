
import unittest, json
from webtest import TestApp
from .app import User
from .app import application


def build_url(id_=None, params=None):
    base = 'http://localhost:8080/api/user'
    if params:
        base = base + params
    return base + '/' + id_ if id_ else base


class TestIntegrated(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)

    def test_columns(self):
        self.assertEqual(['age', 'id', 'name'], User.columns())

    def _create(self, name=None, age=None):
        return self.app.post_json(build_url(), {'age': age, 'name': name})

    def test_api(self):
        # test post create
        resp = self._create(name='felipe', age=22)
        result = resp.json['result']

        self.assertEqual(result['name'], 'felipe')
        self.assertEqual(result['age'], 22)
        self.assertIsNotNone(result['id'])
        id_created = str(result['id'])

        self._create(name='john', age=26)

        # test get all
        resp = self.app.get(build_url())
        result = resp.json['result']

        names = ['felipe', 'john']
        for user in result:
            self.assertTrue(user['name'] in names)
            self.assertIsNotNone(user['id'])

        # test get by id
        resp = self.app.get(build_url(id_created))
        result = resp.json['result']
        self.assertEqual('felipe', result['name'])
        self.assertEqual(22, result['age'])

        # test update
        resp = self.app.put_json(build_url(id_created), {'name': 'felipe volpone'})
        self.assertEqual(200, resp.status_int)

        resp = self.app.get(build_url(id_created))
        result = resp.json['result']
        self.assertEqual('felipe volpone', result['name'])
        self.assertEqual(22, result['age'])
        self.assertEqual(int(id_created), result['id'])

        # test delete
        resp = self.app.delete(build_url(id_created))
        self.assertEqual(200, resp.status_int)

        # test get
        resp = self.app.get(build_url(id_created), expect_errors=True)
        self.assertEqual(404, resp.status_int)


class TestWhereAtAPI(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)

    def _create(self, name=None, age=None):
        return self.app.post_json(build_url(), {'age': age, 'name': name})

    def test_query_params(self):
        for name, age in [('felipe', 35), ('joao', 23), ('roberto', 55), ('roberto', 53)]:
            self._create(name=name, age=age)

        resp = self.app.get(build_url(params="?name=felipe"))
        self.assertEqual(200, resp.status_int)
        result = resp.json['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 35)

        resp = self.app.get(build_url(params="?age=23"))
        self.assertEqual(200, resp.status_int)
        result = resp.json['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'joao')

        resp = self.app.get(build_url(params="?name=roberto"))
        self.assertEqual(200, resp.status_int)
        result = resp.json['result']
        self.assertEqual(2, len(result))
        self.assertEqual(result[0]['age'], 55)
        self.assertEqual(result[1]['age'], 53)

        resp = self.app.get(build_url(params="?name=roberto&age=53"))
        self.assertEqual(200, resp.status_int)
        result = resp.json['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'roberto')
        self.assertEqual(result[0]['age'], 53)
