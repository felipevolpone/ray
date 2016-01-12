from onhands.api import OnHandsSettings, app
from onhands.http import Request
from onhands.actions import ActionAPI, action
from onhands.model import Model
from alabama.models import StringProperty
from tests.mock import TestMock


class UserModel(Model):
    name = StringProperty()


class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("activate")
    def activate_user(self, uuid):
        print uuid


class TestAction(TestMock):

    def setUp(self):
        OnHandsSettings.ACTION_MODULES = 'tests.test_actions'

    def test_action(self):
        request = Request.blank('/api/user/123/activate', method='PUT')
        response = request.get_response(app)
        self.assertEqual(200, response.status_int)
