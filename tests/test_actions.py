from onhands.api import OnHandsSettings, app
from onhands.http import Request
from onhands.actions import ActionAPI, action
from onhands.model import Model
from onhands.endpoint import endpoint
from alabama.models import StringProperty
from tests.mock import TestMock, MockResponse


@endpoint('/user')
class UserModel(Model):
    name = StringProperty()


any_number = 10


class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("/activate")
    def activate_user(self, id_):
        # just to make sure that this method was called
        global any_number
        any_number = id_
        return 'activate_user'


class TestAction(TestMock):

    def setUp(self):
        OnHandsSettings.ACTION_MODULES = 'tests.test_actions'

    def test_get_action(self):
        self.assertEqual('activate_user', ActionAPI.get_action('/activate', 'user', '123'))

    def __create(self):
        OnHandsSettings.ENDPOINT_MODULES = 'tests.test_endpoint'
        request = Request.blank('/api/user', method='POST')
        request.json = {"name": "felipe"}
        return MockResponse(request.get_response(app))

    def test_action(self):
        response = self.__create()
        user_id = response.to_json()['result']['uuid']

        request = Request.blank('/api/user/'+user_id+'/activate', method='PUT')
        response = request.get_response(app)
        self.assertEqual(200, response.status_int)

        global any_number
        self.assertEqual(user_id, any_number)
