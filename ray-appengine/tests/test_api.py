
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
        pass
