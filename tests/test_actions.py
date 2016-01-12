from onhands.api import OnHandsSettings, app
from onhands.http import Request
from onhands.actions import ActionAPI
from onhands.model import Model
from alabama.models import StringProperty
from tests.mock import TestMock


class UserModel(Model):
    name = StringProperty()


class ActionUser(ActionAPI):
    __model__ = UserModel


class TestAction(TestMock):
    
    def setUp(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_action'

    def test_action(self):
        request = Request.blank('/api/user/activate', method='PUT')
        response = request.get_response(app)
        self.assertEqual(200, response.status_int)

    def __create(self):
        request = Request.blank('/api/user', method='POST')
        request.json = {"name": "felipe", "age": 22}
        return request.get_response(app)
