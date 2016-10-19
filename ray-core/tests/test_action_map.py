from ray.actions import ActionAPI, action
from ray.application import ray_conf

from tests.common import UserModel
import unittest


class UserAction(ActionAPI):
    __model__ = UserModel

    @action('activate')
    def activate(self, parameters):
        pass


class TestActionMapping(unittest.TestCase):

    def test(self):
        self.assertTrue('user/activate' in ray_conf['action'])
