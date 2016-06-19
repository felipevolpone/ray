
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

    def test_put(self, name=None, age=None):
        pass
