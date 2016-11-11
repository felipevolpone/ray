from ray.endpoint import endpoint
from tests.model_interface import ModelInterface
from ray.wsgi.wsgi import application

import unittest
from webtest import TestApp as FakeApp


@endpoint('/user')
class UserModel(ModelInterface):

    def __init__(self, *a, **k):
        self.name = None
        self.age = None
        super(UserModel, self).__init__(*a, **k)

    @classmethod
    def columns(cls):
        return ['age', 'id', 'name']


class Test(unittest.TestCase):

    def setUp(self):
        self.app = FakeApp(application)
