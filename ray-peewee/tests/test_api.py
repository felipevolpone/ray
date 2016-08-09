
import unittest, peewee
from ray_peewee.all import PeeweeModel

import unittest
import json
from webapp2 import Request
from ray.http import Response
from ray.wsgi.wsgi import application
from ray.endpoint import endpoint


database = peewee.SqliteDatabase('example.db')


class DBModel(PeeweeModel):
    class Meta:
        database = database


@endpoint('/user')
class User(DBModel):
    name = peewee.CharField()
    age = peewee.IntegerField()


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


class TestRayPeeweeAPI(unittest.TestCase):

    def setUp(self):
        database.drop_tables([User], safe=True)
        database.create_tables([User])

    def test_columns(self):
        self.assertEqual(['age', 'id', 'name'], User.columns())

    def test_to_instance(self):
        new_user = User.to_instance({'age': 99, 'name': 'Frank Sinatra'})
        self.assertEqual(99, new_user.age)
        self.assertEqual('Frank Sinatra', new_user.name)

    def test_database_methods(self):
        user = User.create(name='felipe', age=100)

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
        resp = req.get_response(application)
        self.assertEqual(200, resp.status_code)

        # testing if update worked
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
