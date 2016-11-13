
import unittest, peewee, json
from ray_peewee.all import PeeweeModel

from webtest import TestApp
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


def build_url(id_=None, params=None):
    base = 'http://localhost:8080/api/user'
    if params:
        base = base + params
    return base + '/' + id_ if id_ else base


class TestRayPeeweeAPI(unittest.TestCase):

    def setUp(self):
        database.drop_tables([User], safe=True)
        database.create_tables([User])

        self.app = TestApp(application)

    def test_columns(self):
        self.assertEqual(['age', 'id', 'name'], User.columns())

    def test_to_instance(self):
        new_user = User.to_instance({'age': 99, 'name': 'Frank Sinatra'})
        self.assertEqual(99, new_user.age)
        self.assertEqual('Frank Sinatra', new_user.name)

    def test_database_methods(self):
        User.create(name='felipe', age=100)

    def _create(self, name=None, age=None):
        return self.app.post_json(build_url(), {'age': age, 'name': name})

    def test_api(self):
        # test post create
        resp = self._create(name='felipe', age=23)
        result = resp.json['result']
        self.assertEqual(result['name'], 'felipe')
        self.assertEqual(result['age'], 23)
        self.assertIsNotNone(result['id'])
        id_created = str(result['id'])

        self._create(name='john', age=26)

        # test get all
        resp = self.app.get(build_url())
        result = resp.json['result']

        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 23)
        self.assertIsNotNone(result[0]['id'])
        self.assertEqual(result[1]['name'], 'john')

        # test get by id
        resp = self.app.get(build_url(id_created))
        result = resp.json['result']
        self.assertEqual('felipe', result['name'])
        self.assertEqual(23, result['age'])

        resp = self.app.get(build_url(params="?name=felipe"))
        self.assertEqual(200, resp.status_int)
        result = resp.json['result']
        self.assertEqual(1, len(result))
        self.assertEqual(result[0]['name'], 'felipe')
        self.assertEqual(result[0]['age'], 23)

        # test update
        resp = self.app.put_json(build_url(id_created), {'name': 'felipe volpone'})
        self.assertEqual(200, resp.status_int)

        # testing if update worked
        resp = self.app.get(build_url(id_created))
        result = resp.json['result']
        self.assertEqual('felipe volpone', result['name'])
        self.assertEqual(23, result['age'])
        self.assertEqual(int(id_created), result['id'])

        # test delete
        resp = self.app.delete(build_url(id_created))
        self.assertEqual(200, resp.status_int)

        # test get
        resp = self.app.get(build_url(id_created), expect_errors=True)
        self.assertEqual(404, resp.status_int)
