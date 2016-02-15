import unittest

from webapp2 import Request

from onhands.wsgi.wsgi import application
from onhands.actions import ActionAPI, action
from onhands.endpoint import endpoint

from tests.model_interface import ModelInterface


@endpoint('/user')
class UserModel(ModelInterface):

    def __init__(self, *a, **k):
        self.name = None
        self.age = None
        super(UserModel, self).__init__(*a, **k)

    def describe(self):
        return {'name': str, 'age': int}


any_number = 10


class ActionUser(ActionAPI):
    __model__ = UserModel

    @action("/activate")
    def activate_user(self, model_id):
        # just to make sure that this method was called
        global any_number
        any_number = model_id
        return 'activate_user'


class TestAction(unittest.TestCase):

    def test_get_action(self):
        self.assertEqual('activate_user', ActionAPI.get_action('user', 'activate', '123'))

    def test_action(self):
        user_id = '12312'

        request = Request.blank('/api/user/' + user_id + '/activate', method='POST')
        response = request.get_response(application)
        self.assertEqual(200, response.status_int)

        global any_number
        self.assertEqual(user_id, any_number)

    def test_action_url_404(self):
        request = Request.blank('/api/user/123/dontexists', method='POST')
        response = request.get_response(application)
        self.assertEqual(404, response.status_int)
