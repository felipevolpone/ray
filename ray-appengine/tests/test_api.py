
from webapp2 import Request, Response
import requests, unittest, json
from google.appengine.ext import ndb
from ray_appengine.all import GAEModel
from .gae_test import TestCreateEnviroment
from ray.endpoint import endpoint, RaySettings


RaySettings.ENDPOINT_MODULES.append('test_api')


@endpoint('/post')
class User(GAEModel):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()


class TestIntegrated(TestCreateEnviroment):

    def test_columns(self):
        columns = User.columns()
        self.assertEqual(['age', 'name'], columns)

    def test_put(self):
        new_user = User(name='john', age=25).put()

        all_users = User.query().fetch()
        self.assertEqual(1, len(all_users))

    def test_delete(self):
        # setup
        new_user = User(name='john', age=25)
        new_user.put()
        all_users = User.query().fetch()
        self.assertEqual(1, len(all_users))

        # delete
        new_user.remove()
        all_users = User.query().fetch()
        self.assertEqual(0, len(all_users))

    def test_find(self):
        # setup
        for name, age in [('john', 30), ('maria', 40), ('some', 50), ('felipe', 40)]:
            User(name=name, age=age).put()

        # testing one param
        result = User.find(name='maria')
        self.assertEqual(result, [{'age': 40, 'name': u'maria'}])

        # testing select all
        result = User.find()
        self.assertEqual(result, [{'age': 30, 'name': u'john'}, {'age': 40, 'name': u'maria'},
                                  {'age': 50, 'name': u'some'}, {'name': 'felipe', 'age': 40}])

        # testing one param with more than one result
        result = User.find(age=40)
        self.assertEqual(result, [{'age': 40, 'name': u'maria'}, {'name': 'felipe', 'age': 40}])

        # testing two param with more than one result
        result = User.find(age=40, name='maria')
        self.assertEqual(result, [{'age': 40, 'name': u'maria'}])

    def test_get(self):
        ids = []
        for name, age in [('john', 30), ('maria', 40), ('some', 50), ('felipe', 40)]:
            ids.append(User(name=name, age=age).put().id())

        user = User.get(ids[0])
        self.assertEqual('john', user.name)
